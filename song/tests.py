import os
import datetime
import jwt
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from .models import User, Song
from user.tests import generate_token


class GetUserSongsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_user_songs')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.song1 = Song.objects.create(
            title='Song 1',
            uploader=self.user,
            visible=True,
            cover='covers/test_cover.jpg',
            audio='audios/test_audio.mp3'
        )
        self.song2 = Song.objects.create(
            title='Song 2',
            uploader=self.user,
            visible=False
        )
        self.token = generate_token('testuser', 'user')

        # 创建必要的文件
        self.cover_path = os.path.join(settings.MEDIA_ROOT, 'covers/test_cover.jpg')
        self.audio_path = os.path.join(settings.MEDIA_ROOT, 'audios/test_audio.mp3')
        os.makedirs(os.path.dirname(self.cover_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.audio_path), exist_ok=True)

        # 创建一个有效的图像文件
        image = Image.new('RGB', (100, 100))
        image.save(self.cover_path)

        with open(self.audio_path, 'w') as f:
            f.write('test audio content')

    def test_get_user_songs_missing_username(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少用户姓名'})

    def test_get_user_songs_user_not_exist(self):
        response = self.client.get(self.url, {'username': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '用户不存在'})

    def test_get_user_songs_success(self):
        response = self.client.get(self.url, {'username': 'testuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取用户歌曲成功')
        self.assertEqual(len(response.json()['data']), 1)
        self.assertEqual(response.json()['data'][0]['title'], 'Song 1')

    def test_get_user_songs_internal_server_error(self):
        original_get = User.objects.get
        User.objects.get = lambda *args, **kwargs: 1 / 0  # exception

        response = self.client.get(self.url, {'username': 'testuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['success'], False)

        User.objects.get = original_get

    def test_get_user_songs_missing_token(self):
        response = self.client.get(self.url, {'username': 'testuser'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Authorization header missing'})

    def test_get_user_songs_invalid_token(self):
        response = self.client.get(self.url, {'username': 'testuser'}, HTTP_AUTHORIZATION='Bearer invalid_token')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Invalid token'})

    def tearDown(self):
        self.user.delete()
        self.song1.delete()
        self.song2.delete()
        if os.path.exists(self.cover_path):
            os.remove(self.cover_path)
        if os.path.exists(self.audio_path):
            os.remove(self.audio_path)
