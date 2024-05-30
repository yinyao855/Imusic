import os
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from .models import User, SongList
from user.tests import generate_token


class GetUserSonglistsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_user_songlists')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.songlist1 = SongList.objects.create(
            title='Songlist 1',
            owner=self.user,
            visible=True
        )
        self.songlist2 = SongList.objects.create(
            title='Songlist 2',
            owner=self.user,
            visible=False
        )
        self.token = generate_token('testuser', 'user')

    def test_get_user_songlists_missing_username(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少用户姓名'})

    def test_get_user_songlists_user_not_exist(self):
        response = self.client.get(self.url, {'username': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '用户不存在'})

    def test_get_user_songlists_success(self):
        response = self.client.get(self.url, {'username': 'testuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取用户歌单成功')
        self.assertEqual(len(response.json()['data']), 1)
        self.assertEqual(response.json()['data'][0]['title'], 'Songlist 1')

    def test_get_user_songlists_missing_token(self):
        response = self.client.get(self.url, {'username': 'testuser'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Authorization header missing'})

    def test_get_user_songlists_invalid_token(self):
        response = self.client.get(self.url, {'username': 'testuser'}, HTTP_AUTHORIZATION='Bearer invalid_token')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Invalid token'})

    def tearDown(self):
        self.user.delete()
        self.songlist1.delete()
        self.songlist2.delete()


class SonglistCreateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.token = generate_token('testuser', 'user')

        # 使用本地文件
        self.cover_path = os.path.join(settings.MEDIA_ROOT, 'covers/test.jpg')

        with open(self.cover_path, 'rb') as f:
            self.cover = SimpleUploadedFile('cover.jpg', f.read(), content_type='image/jpeg')

    def test_songlist_create_missing_fields(self):
        data = {
            'title': 'Test Songlist',
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少字段：owner'})

    def test_songlist_create_missing_cover(self):
        data = {
            'title': 'Test Songlist',
            'owner': 'testuser'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少封面图'})

    def test_songlist_create_existing_songlist(self):
        SongList.objects.create(
            title='Test Songlist',
            owner=self.user,
            cover=self.cover
        )
        data = {
            'title': 'Test Songlist',
            'owner': 'testuser',
            'cover': self.cover
        }
        files = {
            'cover': self.cover
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, files=files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '歌单已存在'})

    def test_songlist_create_owner_not_exist(self):
        data = {
            'title': 'Test Songlist',
            'owner': 'nonexistentuser',
            'cover': self.cover
        }
        files = {
            'cover': self.cover
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, files=files)
        self.assertEqual(response.json(), {'success': False, 'message': '所有者不存在'})
        self.assertEqual(response.status_code, 404)

    def test_songlist_create_success(self):
        data = {
            'title': 'Test Songlist',
            'owner': 'testuser',
            'tag_language': '国语',
            'introduction': 'This is a test songlist',
            'cover': self.cover
        }
        files = {
            'cover': self.cover
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, files=files)
        self.assertEqual(response.json()['message'], '歌单创建成功')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['success'], True)
        self.assertTrue(SongList.objects.filter(title='Test Songlist', owner=self.user).exists())

    def test_songlist_create_missing_token(self):
        data = {
            'title': 'Test Songlist',
            'owner': 'testuser',
            'cover': self.cover
        }
        files = {
            'cover': self.cover
        }
        response = self.client.post(self.url, data, files=files)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Authorization header missing'})

    def test_songlist_create_invalid_token(self):
        data = {
            'title': 'Test Songlist',
            'owner': 'testuser',
            'cover': self.cover
        }
        files = {
            'cover': self.cover
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION='Bearer invalid_token', files=files)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Invalid token'})

    def tearDown(self):
        self.user.delete()
        SongList.objects.all().delete()