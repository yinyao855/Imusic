import os
from unittest.mock import patch, mock_open
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from user.models import User
from singer.models import Singer
from user.tests import generate_token
from song.tests import delete_files_except

cover_directory = os.path.join(settings.MEDIA_ROOT, 'covers/')
audio_directory = os.path.join(settings.MEDIA_ROOT, 'audios/')
exception_cover_file = 'test.jpg'
exception_audio_file = 'test.mp3'


class SingerUpdateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.regular_user = User.objects.create(
            username='regularuser',
            email='regularuser@example.com',
            password='password',
            role='user'
        )
        self.singer = Singer.objects.create(
            singerID=1,
            singerName='Original Singer',
            singerImage='singers/original_image.jpg'
        )
        self.url = reverse('update', kwargs={'singerid': self.singer.singerID})
        self.admin_token = generate_token('adminuser', 'admin')
        self.regular_token = generate_token('regularuser', 'user')

        self.original_image_path = os.path.join(settings.MEDIA_ROOT, 'covers/test.jpg')
        self.new_image_path = self.original_image_path

    def test_singer_update_success(self):
        data = {
            'singerName': 'Updated Singer'
        }
        with open(self.new_image_path, 'rb') as f:
            files = {
                'singerImage': SimpleUploadedFile('new_image.jpg', f.read(), content_type='image/jpeg')
            }
            response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.admin_token, **files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '更新成功')
        self.singer.refresh_from_db()
        self.assertEqual(self.singer.singerName, 'Updated Singer')

    def test_singer_update_no_permission(self):
        data = {
            'singerName': 'Updated Singer'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.regular_token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'message': '没有权限操作'})
        self.singer.refresh_from_db()
        self.assertEqual(self.singer.singerName, 'Original Singer')

    def test_singer_update_file_replacement(self):
        data = {
            'singerName': 'Updated Singer'
        }
        with open(self.new_image_path, 'rb') as f:
            files = {
                'singerImage': SimpleUploadedFile('new_image.jpg', f.read(), content_type='image/jpeg')
            }
            response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.admin_token, **files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '更新成功')
        self.singer.refresh_from_db()
        self.assertEqual(self.singer.singerName, 'Updated Singer')

    def test_singer_update_nonexistent_singer(self):
        url = reverse('update', kwargs={'singerid': 999})
        data = {
            'singerName': 'Updated Singer'
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.admin_token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '歌手不存在'})

    def tearDown(self):
        self.admin_user.delete()
        self.regular_user.delete()
        self.singer.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)
