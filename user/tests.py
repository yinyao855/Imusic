import os
import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import jwt
from .models import User
from user.utils import validate_verification_code


class UserRegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user_register')
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'password'
        self.avatar = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.bio = 'This is a test bio.'
        self.verification_code = '123456'

        self.token = jwt.encode({
            'username': self.username,
            'verification_code': self.verification_code,
            'role': 'user'
        }, settings.SECRET_KEY, algorithm='HS256')

        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

    def test_register_missing_fields(self):
        response = self.client.post(self.url, {
            'username': self.username,
            'password': self.password
            # 缺少 'verification_code'
        }, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少字段：verification_code'})

    def test_register_user_already_exists(self):
        User.objects.create(username=self.username, email=self.email, password=self.password)
        response = self.client.post(self.url, {
            'username': self.username,
            'password': self.password,
            'verification_code': self.verification_code
        }, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': False, 'message': '用户名已存在'})

    def test_register_invalid_verification_code(self):
        response = self.client.post(self.url, {
            'username': self.username,
            'password': self.password,
            'verification_code': 'wrong_code'
        }, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': False, 'message': '验证码错误或已失效'})

    def test_register_success(self):
        response = self.client.post(self.url, {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'avatar': self.avatar,
            'bio': self.bio,
            'verification_code': self.verification_code
        }, **self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'success': True, 'message': '注册成功'})
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_jwt_middleware_missing_authorization_header(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Authorization header missing'})

    def test_jwt_middleware_invalid_token(self):
        headers = {'HTTP_AUTHORIZATION': 'Bearer invalid_token'}
        response = self.client.get(self.url, **headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Invalid token'})

    def test_jwt_middleware_expired_token(self):
        expired_token = jwt.encode({
            'username': self.username,
            'verification_code': self.verification_code,
            'role': 'user',
            'exp': 0  # Token 过期
        }, settings.SECRET_KEY, algorithm='HS256')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {expired_token}'}
        response = self.client.get(self.url, **headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Token expired'})

    def test_jwt_middleware_valid_token(self):
        response = self.client.get(self.url, **self.headers)
        self.assertNotEqual(response.status_code, 401)

    def test_validate_verification_code(self):
        request = self.client.post(self.url, {
            'username': self.username,
            'password': self.password,
            'verification_code': self.verification_code
        }, **self.headers).wsgi_request
        request.token_verification_code = self.verification_code
        self.assertTrue(validate_verification_code(request, self.verification_code))
        self.assertFalse(validate_verification_code(request, 'wrong_code'))


class UserLoginTestCase(TestCase):

    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            role='user'
        )
        self.client = Client()
        self.url = reverse('user_login')

    def test_successful_login(self):
        # 成功登录的测试
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('message'), '登录成功')
        self.assertIn('token', response.json())

    def test_invalid_username(self):
        # 测试无效的用户名
        response = self.client.post(self.url, {'username': 'invaliduser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '用户名或密码错误')

    def test_invalid_password(self):
        # 测试无效的密码
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '用户名或密码错误')

    def test_token_generation(self):
        # 测试token生成
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword'})
        token = response.json().get('token')
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        self.assertEqual(decoded_token['user_id'], self.user.user_id)
        self.assertEqual(decoded_token['username'], self.user.username)
        self.assertEqual(decoded_token['role'], self.user.role)

    def test_user_data_in_response(self):
        # 测试返回数据
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword'})
        data = response.json().get('data')
        self.assertEqual(data['user_id'], self.user.user_id)
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)

    def tearDown(self):
        # 清理测试数据
        self.user.delete()


def generate_token(username, role, verification_code=None):
    # 生成测试用的JWT token
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=3)
    }
    if verification_code:
        payload['verification_code'] = verification_code
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return f'Bearer {token}'

class GetUserInfoTestCase(TestCase):

    def setUp(self):
        # 创建测试用户
        self.admin_user = User.objects.create(
            username='adminuser',
            password='adminpassword',
            email='adminuser@example.com',
            role='admin'
        )
        self.normal_user = User.objects.create(
            username='normaluser',
            password='normalpassword',
            email='normaluser@example.com',
            role='user'
        )
        self.client = Client()

    def test_get_user_info_as_admin(self):
        # 模拟admin用户获取用户信息
        token = generate_token('adminuser', 'admin')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('get_user_info', kwargs={'username': 'normaluser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('message'), '获取用户信息成功')
        data = response.json().get('data')
        self.assertEqual(data['username'], 'normaluser')
        self.assertEqual(data['email'], 'normaluser@example.com')

    def test_get_user_info_as_self(self):
        # 模拟普通用户获取自己的信息
        token = generate_token('normaluser', 'user')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('get_user_info', kwargs={'username': 'normaluser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('message'), '获取用户信息成功')
        data = response.json().get('data')
        self.assertEqual(data['username'], 'normaluser')
        self.assertEqual(data['email'], 'normaluser@example.com')

    def test_get_user_info_as_other_user(self):
        # 模拟普通用户获取其他用户的信息
        other_user = User.objects.create(
            username='otheruser',
            password='otherpassword',
            email='otheruser@example.com',
            role='user'
        )
        token = generate_token('normaluser', 'user')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('get_user_info', kwargs={'username': 'otheruser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('message'), '获取用户信息成功')
        data = response.json().get('data')
        self.assertEqual(data['username'], 'otheruser')
        self.assertEqual(data.get('email'), 'otheruser@example.com')

    def test_get_user_info_user_not_exist(self):
        # 测试获取不存在的用户信息
        token = generate_token('adminuser', 'admin')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('get_user_info', kwargs={'username': 'nonexistentuser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '用户不存在')

    def tearDown(self):
        # 清理测试数据
        self.admin_user.delete()
        self.normal_user.delete()




class UpdateUserInfoTestCase(TestCase):

    def setUp(self):
        # 创建测试用户
        self.admin_user = User.objects.create(
            username='adminuser',
            password='adminpassword',
            email='adminuser@example.com',
            role='admin'
        )
        self.normal_user = User.objects.create(
            username='normaluser',
            password='normalpassword',
            email='normaluser@example.com',
            role='user'
        )
        self.client = Client()

    def test_update_user_info_success(self):
        # 模拟admin用户成功更新信息
        token = generate_token('adminuser', 'admin')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('update_user_info', kwargs={'username': 'normaluser'})
        response = self.client.post(url, {
            'email': 'updated@example.com',
            'bio': 'Updated bio'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('message'), '用户信息修改成功')
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.email, 'updated@example.com')
        self.assertEqual(self.normal_user.bio, 'Updated bio')

    def test_update_user_info_user_not_exist(self):
        # 测试更新不存在的用户信息
        token = generate_token('adminuser', 'admin')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('update_user_info', kwargs={'username': 'nonexistentuser'})
        response = self.client.post(url, {
            'email': 'updated@example.com',
            'bio': 'Updated bio'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '用户不存在')

    def test_update_user_info_no_permission(self):
        # 模拟普通用户试图更新其他用户的信息
        token = generate_token('normaluser', 'user')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('update_user_info', kwargs={'username': 'adminuser'})
        response = self.client.post(url, {
            'email': 'updated@example.com',
            'bio': 'Updated bio'
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '没有权限操作')

    def test_update_user_info_validation_error(self):
        # 模拟更新信息时出现验证错误
        token = generate_token('adminuser', 'admin')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('update_user_info', kwargs={'username': 'normaluser'})
        response = self.client.post(url, {
            'email': 'invalid-email'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('success'), False)

    def tearDown(self):
        # 清理测试数据
        self.admin_user.delete()
        self.normal_user.delete()




class DeleteUserTestCase(TestCase):

    def setUp(self):
        # 创建测试用户
        self.admin_user = User.objects.create(
            username='adminuser',
            password='adminpassword',
            email='adminuser@example.com',
            role='admin'
        )
        self.normal_user = User.objects.create(
            username='normaluser',
            password='normalpassword',
            email='normaluser@example.com',
            role='user',
            avatar='avatars/test_avatar.jpg'
        )
        # 创建虚拟头像文件
        self.avatar_path = os.path.join(settings.MEDIA_ROOT, 'avatars/test_avatar.jpg')
        os.makedirs(os.path.dirname(self.avatar_path), exist_ok=True)
        with open(self.avatar_path, 'w') as f:
            f.write('test image content')

        self.client = Client()

    def test_delete_user_success(self):
        # 模拟用户成功删除自己的账号
        token = generate_token('normaluser', 'user')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('delete_user', kwargs={'username': 'normaluser'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('message'), '用户删除成功')
        self.assertFalse(User.objects.filter(username='normaluser').exists())
        self.assertFalse(os.path.exists(self.avatar_path))


    def test_delete_user_no_permission(self):
        # 模拟普通用户试图删除其他用户的账号
        token = generate_token('normaluser', 'user')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('delete_user', kwargs={'username': 'adminuser'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '没有权限操作')

    def test_delete_user_avatar_deletion(self):
        # 测试删除用户时删除其头像文件
        token = generate_token('normaluser', 'user')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('delete_user', kwargs={'username': 'normaluser'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('message'), '用户删除成功')
        self.assertFalse(User.objects.filter(username='normaluser').exists())
        self.assertFalse(os.path.exists(self.avatar_path))

    def tearDown(self):
        # 清理测试数据
        if os.path.exists(self.avatar_path):
            os.remove(self.avatar_path)
        self.admin_user.delete()
        self.normal_user.delete()




class ChangeUserRoleTestCase(TestCase):

    def setUp(self):
        # 创建测试用户
        self.admin_user = User.objects.create(
            username='adminuser',
            password='adminpassword',
            email='adminuser@example.com',
            role='admin'
        )
        self.normal_user = User.objects.create(
            username='normaluser',
            password='normalpassword',
            email='normaluser@example.com',
            role='user'
        )
        self.other_user = User.objects.create(
            username='otheruser',
            password='otherpassword',
            email='otheruser@example.com',
            role='user'
        )
        self.client = Client()

        # 创建授权密钥文件
        self.authorized_key = 'test_key'
        with open('authorized_key', 'w') as f:
            f.write(self.authorized_key)

    def test_change_user_role_success_as_admin(self):
        # 模拟管理员用户成功修改角色
        token = generate_token('adminuser', 'admin')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('change_user_role')
        response = self.client.post(url, {
            'dir_user': 'normaluser',
            'role': 'admin'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('message'), '用户权限修改成功')
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.role, 'admin')

    def test_change_user_role_success_with_key(self):
        # 模拟使用授权密钥成功修改角色
        token = generate_token('normaluser', 'user')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('change_user_role')
        response = self.client.post(url, {
            'dir_user': 'otheruser',
            'role': 'admin',
            'key': self.authorized_key
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('message'), '用户权限修改成功')
        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.role, 'admin')

    def test_change_user_role_user_not_exist(self):
        # 测试修改不存在的用户角色
        token = generate_token('adminuser', 'admin')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('change_user_role')
        response = self.client.post(url, {
            'dir_user': 'nonexistentuser',
            'role': 'admin'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '用户不存在')

    def test_change_user_role_permission_denied(self):
        # 模拟普通用户试图修改其他用户角色，权限不足
        token = generate_token('normaluser', 'user')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('change_user_role')
        response = self.client.post(url, {
            'dir_user': 'otheruser',
            'role': 'admin'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '用户权限修改失败，权限不足')

    def test_change_user_role_invalid_role(self):
        # 测试修改角色为无效角色
        token = generate_token('adminuser', 'admin')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('change_user_role')
        response = self.client.post(url, {
            'dir_user': 'normaluser',
            'role': 'invalidrole'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '用户权限修改失败，权限错误')

    def tearDown(self):
        # 清理测试数据
        self.admin_user.delete()
        self.normal_user.delete()
        self.other_user.delete()
        if os.path.exists('authorized_key'):
            os.remove('authorized_key')


def mock_validate_verification_code(request, code):
    return request.token_verification_code == code

class ChangePasswordTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Mock validate_verification_code 函数
        cls.original_validate_verification_code = globals()['validate_verification_code']
        globals()['validate_verification_code'] = mock_validate_verification_code

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # 还原 validate_verification_code 函数
        globals()['validate_verification_code'] = cls.original_validate_verification_code

    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create(
            username='testuser',
            password='oldpassword',
            email='testuser@example.com'
        )
        self.client = Client()

    def test_change_password_success(self):
        # 模拟成功修改密码
        token = generate_token('testuser', 'user', 'valid_code')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        url = reverse('change_password')
        response = self.client.post(url, {
            'username': 'testuser',
            'new_password': 'newpassword',
            'verification_code': 'valid_code'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('message'), '密码修改成功')
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, 'newpassword')


    def test_change_password_missing_field(self):
        # 模拟缺少必填字段
        url = reverse('change_password')
        token = generate_token('testuser', 'user')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        response = self.client.post(url, {
            'username': 'testuser',
            'new_password': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '缺少字段：verification_code')

    def test_change_password_invalid_code(self):
        # 模拟验证码错误或已失效
        url = reverse('change_password')
        token = generate_token('testuser', 'user')
        self.client.defaults['HTTP_AUTHORIZATION'] = token
        response = self.client.post(url, {
            'username': 'testuser',
            'new_password': 'newpassword',
            'verification_code': 'invalid_code'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), '验证码错误或已失效')

    def tearDown(self):
        # 清理测试数据
        self.user.delete()


