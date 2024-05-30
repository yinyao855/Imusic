import os

from django.http import JsonResponse
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from unittest.mock import patch

from like.models import LikedSongList
from .models import User, SongList
from song.models import Song
from user.tests import generate_token
from song.tests import delete_files_except

cover_directory = os.path.join(settings.MEDIA_ROOT, 'covers/')
audio_directory = os.path.join(settings.MEDIA_ROOT, 'audios/')
exception_cover_file = 'test.jpg'
exception_audio_file = 'test.mp3'


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
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


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
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class GetSonglistInfoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.user,
            cover='covers/test_cover.jpg',
            audio='audios/test_audio.mp3'
        )
        self.songlist = SongList.objects.create(
            title='Test SongList',
            owner=self.user,
            cover='covers/test_cover.jpg',
            introduction='This is a test song list.'
        )
        self.songlist.songs.add(self.song)
        self.url = reverse('get_songlist_info', kwargs={'songlistID': self.songlist.id})
        self.token = generate_token('testuser', 'user')

        self.cover_path = os.path.join(settings.MEDIA_ROOT, 'covers/test.jpg')
        self.audio_path = os.path.join(settings.MEDIA_ROOT, 'audios/test.mp3')

    def test_get_songlist_info_success(self):
        response = self.client.get(self.url, {'username': 'testuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取歌单成功')
        self.assertEqual(response.json()['data']['title'], 'Test SongList')

    def test_get_songlist_info_missing_songlist(self):
        url = reverse('get_songlist_info', kwargs={'songlistID': 999})
        response = self.client.get(url, {'username': 'testuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '未找到对应歌单'})

    def test_get_songlist_info_missing_user(self):
        response = self.client.get(self.url, {'username': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '用户不存在'})

    def tearDown(self):
        self.user.delete()
        self.song.delete()
        self.songlist.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class UpdateSonglistInfoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.admin_user = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.cover_path = os.path.join(settings.MEDIA_ROOT, 'covers/test.jpg')
        self.audio_path = os.path.join(settings.MEDIA_ROOT, 'audios/test.mp3')

        with open(self.cover_path, 'rb') as f:
            self.cover = SimpleUploadedFile('cover.jpg', f.read(), content_type='image/jpeg')
        with open(self.audio_path, 'rb') as f:
            self.audio = SimpleUploadedFile('audio.mp3', f.read(), content_type='image/mpeg')

        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.user,
            cover=self.cover,
            audio=self.audio,
        )
        self.songlist = SongList.objects.create(
            title='Test SongList',
            owner=self.user,
            cover=self.cover,
            introduction='This is a test song list.'
        )
        self.songlist.songs.add(self.song)
        self.url = reverse('update_songlist_info', kwargs={'songlistID': self.songlist.id})
        self.token = generate_token('testuser', 'user')
        self.admin_token = generate_token('adminuser', 'admin')

    def test_update_songlist_info_success(self):
        data = {
            'title': 'Updated SongList Title',
            'introduction': 'Updated introduction'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '更新歌单成功')
        updated_songlist = SongList.objects.get(id=self.songlist.id)
        self.assertEqual(updated_songlist.title, 'Updated SongList Title')
        self.assertEqual(updated_songlist.introduction, 'Updated introduction')


    def test_update_nonexistent_songlist(self):
        url = reverse('update_songlist_info', kwargs={'songlistID': 999})
        data = {
            'title': 'Updated SongList Title',
            'introduction': 'Updated introduction'
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '未找到对应歌单'})


    def test_update_songlist_no_permission(self):
        another_user = User.objects.create(
            username='anotheruser',
            email='anotheruser@example.com',
            password='password'
        )
        another_token = generate_token('anotheruser', 'user')
        data = {
            'title': 'Updated SongList Title',
            'introduction': 'Updated introduction'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=another_token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'message': '没有权限操作'})


    def test_update_songlist_missing_data(self):
        data = {}
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '更新歌单成功')
        updated_songlist = SongList.objects.get(id=self.songlist.id)
        self.assertEqual(updated_songlist.title, 'Test SongList')
        self.assertEqual(updated_songlist.introduction, 'This is a test song list.')


    def test_update_songlist_admin_permission(self):
        data = {
            'title': 'Updated SongList Title by Admin',
            'introduction': 'Updated introduction by Admin'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.admin_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '更新歌单成功')
        updated_songlist = SongList.objects.get(id=self.songlist.id)
        self.assertEqual(updated_songlist.title, 'Updated SongList Title by Admin')
        self.assertEqual(updated_songlist.introduction, 'Updated introduction by Admin')


    def tearDown(self):
        self.user.delete()
        self.admin_user.delete()
        self.song.delete()
        self.songlist.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class DeleteSonglistTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.admin_user = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.user,
            cover='covers/test_cover.jpg',
            audio='audios/test_audio.mp3'
        )
        self.songlist = SongList.objects.create(
            title='Test SongList',
            owner=self.user,
            cover='covers/test_cover.jpg',
            introduction='This is a test song list.'
        )
        self.songlist.songs.add(self.song)
        self.url = reverse('delete_songlist', kwargs={'songlistID': self.songlist.id})
        self.token = generate_token('testuser', 'user')
        self.admin_token = generate_token('adminuser', 'admin')

        self.cover_path = os.path.join(settings.MEDIA_ROOT, 'covers/test.jpg')
        self.audio_path = os.path.join(settings.MEDIA_ROOT, 'audios/test.mp3')

        with open(self.cover_path, 'rb') as f:
            self.cover = SimpleUploadedFile('cover.jpg', f.read(), content_type='image/jpeg')
        with open(self.audio_path, 'rb') as f:
            self.audio = SimpleUploadedFile('audio.mp3', f.read(), content_type='image/mpeg')

    def test_delete_songlist_success(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '删除歌单成功')
        self.assertFalse(SongList.objects.filter(id=self.songlist.id).exists())

    def test_delete_nonexistent_songlist(self):
        url = reverse('delete_songlist', kwargs={'songlistID': 999})
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '歌单不存在'})

    def test_delete_songlist_no_permission(self):
        another_user = User.objects.create(
            username='anotheruser',
            email='anotheruser@example.com',
            password='password'
        )
        another_token = generate_token('anotheruser', 'user')
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=another_token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'message': '没有权限操作'})

    def test_delete_songlist_admin_permission(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.admin_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '删除歌单成功')
        self.assertFalse(SongList.objects.filter(id=self.songlist.id).exists())

    def tearDown(self):
        self.user.delete()
        self.admin_user.delete()
        self.song.delete()
        self.songlist.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class SonglistAddTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.admin_user = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.url = reverse('songlist_add')
        self.token = generate_token('testuser', 'user')
        self.admin_token = generate_token('adminuser', 'admin')
        self.cover_path = os.path.join(settings.MEDIA_ROOT, 'covers/test.jpg')
        self.audio_path = os.path.join(settings.MEDIA_ROOT, 'audios/test.mp3')

        with open(self.cover_path, 'rb') as f:
            self.cover = SimpleUploadedFile('cover.jpg', f.read(), content_type='image/jpeg')
        with open(self.audio_path, 'rb') as f:
            self.audio = SimpleUploadedFile('audio.mp3', f.read(), content_type='image/mpeg')

        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.user,
            cover=self.cover,
            audio=self.audio,
        )
        self.songlist = SongList.objects.create(
            title='Test SongList',
            owner=self.user,
            cover=self.cover,
            introduction='This is a test song list.'
        )


    def test_add_song_to_songlist_success(self):
        data = {
            'songlist_id': self.songlist.id,
            'song_id': self.song.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '添加歌曲成功')
        self.assertTrue(self.songlist.songs.filter(id=self.song.id).exists())

    def test_add_song_to_nonexistent_songlist(self):
        data = {
            'songlist_id': 999,
            'song_id': self.song.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '歌单不存在'})

    def test_add_nonexistent_song_to_songlist(self):
        data = {
            'songlist_id': self.songlist.id,
            'song_id': 999
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '某些歌曲未上传，请先上传对应歌曲'})

    def test_add_song_to_songlist_no_permission(self):
        another_user = User.objects.create(
            username='anotheruser',
            email='anotheruser@example.com',
            password='password'
        )
        another_token = generate_token('anotheruser', 'user')
        data = {
            'songlist_id': self.songlist.id,
            'song_id': self.song.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=another_token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'message': '没有权限操作'})

    def test_add_song_to_songlist_admin_permission(self):
        data = {
            'songlist_id': self.songlist.id,
            'song_id': self.song.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.admin_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '添加歌曲成功')
        self.assertTrue(self.songlist.songs.filter(id=self.song.id).exists())

    def tearDown(self):
        self.user.delete()
        self.admin_user.delete()
        self.song.delete()
        self.songlist.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class SonglistRemoveTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.admin_user = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.url = reverse('songlist_add')
        self.token = generate_token('testuser', 'user')
        self.admin_token = generate_token('adminuser', 'admin')
        self.cover_path = os.path.join(settings.MEDIA_ROOT, 'covers/test.jpg')
        self.audio_path = os.path.join(settings.MEDIA_ROOT, 'audios/test.mp3')

        with open(self.cover_path, 'rb') as f:
            self.cover = SimpleUploadedFile('cover.jpg', f.read(), content_type='image/jpeg')
        with open(self.audio_path, 'rb') as f:
            self.audio = SimpleUploadedFile('audio.mp3', f.read(), content_type='image/mpeg')
        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.user,
            cover=self.cover,
            audio=self.audio,
        )
        self.songlist = SongList.objects.create(
            title='Test SongList',
            owner=self.user,
            cover=self.cover,
            introduction='This is a test song list.'
        )
        self.songlist.songs.add(self.song)
        self.url = reverse('songlist_remove')
        self.token = generate_token('testuser', 'user')
        self.admin_token = generate_token('adminuser', 'admin')


    def test_remove_song_from_songlist_success(self):
        data = {
            'songlist_id': self.songlist.id,
            'song_id': self.song.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '删除歌曲成功')
        self.assertFalse(self.songlist.songs.filter(id=self.song.id).exists())

    def test_remove_song_from_nonexistent_songlist(self):
        data = {
            'songlist_id': 999,
            'song_id': self.song.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '歌单不存在'})

    def test_remove_nonexistent_song_from_songlist(self):
        data = {
            'songlist_id': self.songlist.id,
            'song_id': 999
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '某些歌曲未上传，请先上传对应歌曲'})

    def test_remove_song_from_songlist_no_permission(self):
        another_user = User.objects.create(
            username='anotheruser',
            email='anotheruser@example.com',
            password='password'
        )
        another_token = generate_token('anotheruser', 'user')
        data = {
            'songlist_id': self.songlist.id,
            'song_id': self.song.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=another_token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'message': '没有权限操作'})

    def test_remove_song_from_songlist_admin_permission(self):
        data = {
            'songlist_id': self.songlist.id,
            'song_id': self.song.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.admin_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '删除歌曲成功')
        self.assertFalse(self.songlist.songs.filter(id=self.song.id).exists())

    def tearDown(self):
        self.user.delete()
        self.admin_user.delete()
        self.song.delete()
        self.songlist.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)
