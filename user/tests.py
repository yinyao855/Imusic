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
