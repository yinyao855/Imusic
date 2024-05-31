import os
from PIL import Image
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.conf import settings
from like.models import LikedSong
from songlist.models import SongList
from .models import User, Song
from singer.models import Singer
from comment.models import Comment
from complaint.models import Complaint
from user.tests import generate_token


def delete_files_except(directory, exception_file):
    """
    删除指定目录下所有不是 exception_file 的文件。
    """
    files = os.listdir(directory)

    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and file != exception_file:
            try:
                os.remove(file_path)
            except Exception as e:
                # print(f"Error deleting file {file_path}: {e}")
                pass


cover_directory = os.path.join(settings.MEDIA_ROOT, 'covers/')
audio_directory = os.path.join(settings.MEDIA_ROOT, 'audios/')
exception_cover_file = 'test.jpg'
exception_audio_file = 'test.mp3'


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

        self.cover_path = os.path.join(settings.MEDIA_ROOT, 'covers/test.jpg')
        self.audio_path = os.path.join(settings.MEDIA_ROOT, 'audios/test.mp3')

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
        User.objects.get = lambda *args, **kwargs: 1 / 0
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
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class SongUploadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('song_upload')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.token = generate_token('testuser', 'user')

        # 使用本地文件
        self.cover_path = 'media/covers/test.jpg'
        self.audio_path = 'media/audios/test.mp3'
        self.lyric_path = 'media/lyrics/test.lrc'

        with open(self.cover_path, 'rb') as f:
            self.cover = SimpleUploadedFile('cover.jpg', f.read(), content_type='image/jpeg')
        with open(self.audio_path, 'rb') as f:
            self.audio = SimpleUploadedFile('audio.mp3', f.read(), content_type='audio/mpeg')
        with open(self.lyric_path, 'rb') as f:
            self.lyric = SimpleUploadedFile('lyric.txt', f.read(), content_type='text/plain')

    def test_song_upload_missing_fields(self):
        data = {
            'title': 'Test Song',
            'singer': 'Test Singer',
        }
        files = {}
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, format='multipart', **files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少字段：uploader'})

    def test_song_upload_missing_files(self):
        data = {
            'title': 'Test Song',
            'singer': 'Test Singer',
            'uploader': 'testuser'
        }
        files = {}
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, format='multipart', **files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少文件'})

    def test_song_upload_existing_song(self):
        Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.user,
            cover=self.cover,
            audio=self.audio,
        )
        data = {
            'title': 'Test Song',
            'singer': 'Test Singer',
            'uploader': 'testuser',
            'cover': self.cover,
            'audio': self.audio
        }
        files = {
            'cover': self.cover,
            'audio': self.audio
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, format='multipart', **files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '您已经上传过这首歌曲了'})

    def test_song_upload_invalid_audio_format(self):
        invalid_audio = SimpleUploadedFile('test.wav', b'file_content', content_type='audio/wav')
        data = {
            'title': 'Test Song',
            'singer': 'Test Singer',
            'uploader': 'testuser',
            'cover': self.cover,
            'audio': invalid_audio
        }
        files = {
            'cover': self.cover,
            'audio': invalid_audio
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, format='multipart', **files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '音频文件格式必须为MP3'})

    def test_song_upload_large_audio_file(self):
        large_audio = SimpleUploadedFile('large_audio.mp3', b'0' * (25 * 1024 * 1024 + 1), content_type='audio/mpeg')
        data = {
            'title': 'Test Song',
            'singer': 'Test Singer',
            'uploader': 'testuser',
            'cover': self.cover,
            'audio': large_audio
        }
        files = {
            'cover': self.cover,
            'audio': large_audio
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, format='multipart', **files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '音频文件大小超过限制(25MB)'})

    def test_song_upload_large_cover_file(self):
        large_cover = SimpleUploadedFile('large_cover.jpg', b'0' * (10 * 1024 * 1024 + 1), content_type='image/jpeg')
        data = {
            'title': 'Test Song',
            'singer': 'Test Singer',
            'uploader': 'testuser',
            'cover': large_cover,
            'audio': self.audio
        }
        files = {
            'cover': large_cover,
            'audio': self.audio
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, format='multipart', **files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '封面图片大小超过限制(10MB)'})

    def test_song_upload_success(self):
        data = {
            'title': 'Test Song',
            'singer': 'Test Singer',
            'uploader': 'testuser',
            'cover': self.cover,
            'audio': self.audio,
            'lyric': self.lyric
        }
        files = {
            'cover': self.cover,
            'audio': self.audio,
            'lyric': self.lyric
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, format='multipart', **files)
        self.assertEqual(response.json(), {'success': True, 'message': '歌曲上传成功'})
        self.assertEqual(response.status_code, 201)

    def test_song_upload_uploader_not_exist(self):
        data = {
            'title': 'Test Song',
            'singer': 'Test Singer',
            'uploader': 'nonexistentuser',
            'cover': self.cover,
            'audio': self.audio
        }
        files = {
            'cover': self.cover,
            'audio': self.audio
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, format='multipart', **files)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '上传者不存在'})

    def tearDown(self):
        self.user.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class GetSongInfoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_song_info', args=[1])
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.song = Song.objects.create(
            id=1,
            title='Test Song',
            singer='Test Singer',
            cover='covers/test_cover.jpg',
            audio='audios/test_audio.mp3',
            uploader=self.user
        )

    def test_get_song_info_success_without_username(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取歌曲信息成功')
        self.assertEqual(response.json()['data']['title'], 'Test Song')

    def test_get_song_info_success_with_username(self):
        LikedSong.objects.create(user=self.user, song=self.song)
        response = self.client.get(self.url, {'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取歌曲信息成功')
        self.assertEqual(response.json()['data']['title'], 'Test Song')
        self.assertEqual(response.json()['data']['user_like'], True)

    def test_get_song_info_song_not_exist(self):
        url = reverse('get_song_info', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '未找到对应歌曲'})

    def test_get_song_info_user_not_exist(self):
        response = self.client.get(self.url, {'username': 'nonexistentuser'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '用户不存在'})

    def test_get_song_info_internal_server_error(self):
        original_get = Song.objects.get
        Song.objects.get = lambda *args, **kwargs: 1 / 0

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['success'], False)

        Song.objects.get = original_get

    def tearDown(self):
        self.user.delete()
        self.song.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class UpdateSongInfoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('update_song_info', args=[1])
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password',
            role='user'
        )
        self.admin = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.song = Song.objects.create(
            id=1,
            title='Original Title',
            singer='Original Singer',
            uploader=self.user,
            cover='covers/test_cover.jpg',
            audio='audios/test_audio.mp3'
        )
        self.token = generate_token('testuser', 'user')
        self.admin_token = generate_token('adminuser', 'admin')

        self.cover_path = os.path.join(settings.MEDIA_ROOT, 'covers/test.jpg')
        self.audio_path = os.path.join(settings.MEDIA_ROOT, 'audios/test.mp3')
        with open(self.cover_path, 'rb') as f:
            self.cover = SimpleUploadedFile('cover.jpg', f.read(), content_type='image/jpeg')
        with open(self.audio_path, 'rb') as f:
            self.audio = SimpleUploadedFile('audio.mp3', f.read(), content_type='audio/mpeg')

    def test_update_song_info_success(self):
        data = {
            'title': 'New Title',
            'singer': 'New Singer',
            'introduction': 'New Introduction',
            'tag_language': '韩语',
            'cover': self.cover,
            'audio': self.audio
        }
        files = {
            'cover': self.cover,
            'audio': self.audio
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token, format='multipart', **files)
        self.assertEqual(response.json()['message'], '更新成功')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '更新成功')

    def test_update_song_info_song_not_exist(self):
        url = reverse('update_song_info', args=[999])
        response = self.client.post(url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '歌曲未找到'})

    def test_update_song_info_no_permission(self):
        another_user = User.objects.create(
            username='anotheruser',
            email='anotheruser@example.com',
            password='password'
        )
        another_token = generate_token('anotheruser', 'user')
        response = self.client.post(self.url, HTTP_AUTHORIZATION=another_token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'message': '没有权限操作'})

    def test_update_song_info_invalid_data(self):
        response = self.client.post(self.url, {'title': ''}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.json()['message'])

    def tearDown(self):
        self.user.delete()
        self.admin.delete()
        self.song.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class DeleteSongTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('delete_song', args=[1])
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password',
            role='user'
        )
        self.admin = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.song = Song.objects.create(
            id=1,
            title='Test Song',
            singer='Test Singer',
            uploader=self.user,
            cover='covers/test_cover.jpg',
            audio='audios/test_audio.mp3',
            lyric='lyrics/test_lyric.lrc'
        )
        self.token = generate_token('testuser', 'user')
        self.admin_token = generate_token('adminuser', 'admin')

        self.cover_path = os.path.join(settings.MEDIA_ROOT, 'covers/test.jpg')
        self.audio_path = os.path.join(settings.MEDIA_ROOT, 'audios/test.mp3')
        self.lyric_path = os.path.join(settings.MEDIA_ROOT, 'lyrics/test.lrc')
        os.makedirs(os.path.dirname(self.cover_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.audio_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.lyric_path), exist_ok=True)

    def test_delete_song_success_by_uploader(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '删除成功')
        self.assertFalse(Song.objects.filter(id=1).exists())

    def test_delete_song_success_by_admin(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.admin_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '删除成功')
        self.assertFalse(Song.objects.filter(id=1).exists())

    def test_delete_song_not_exist(self):
        url = reverse('delete_song', args=[999])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '歌曲未找到'})

    def test_delete_song_no_permission(self):
        another_user = User.objects.create(
            username='anotheruser',
            email='anotheruser@example.com',
            password='password'
        )
        another_token = generate_token('anotheruser', 'user')
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=another_token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'message': '没有权限操作'})

    def test_delete_song_internal_server_error(self):
        original_delete = Song.delete
        Song.delete = lambda *args, **kwargs: 1 / 0  # 强制引发异常

        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['success'], False)

        Song.delete = original_delete

    def tearDown(self):
        self.user.delete()
        self.admin.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class GetAllSongsTests(TestCase):
    def setUp(self):
        self.cover_path = 'media/covers/test.jpg'
        self.audio_path = 'media/audios/test.mp3'
        self.lyric_path = 'media/lyrics/test.lrc'

        with open(self.cover_path, 'rb') as f:
            self.cover = SimpleUploadedFile('cover.jpg', f.read(), content_type='image/jpeg')
        with open(self.audio_path, 'rb') as f:
            self.audio = SimpleUploadedFile('audio.mp3', f.read(), content_type='audio/mpeg')
        with open(self.lyric_path, 'rb') as f:
            self.lyric = SimpleUploadedFile('lyric.txt', f.read(), content_type='text/plain')

        self.client = Client()
        self.url = reverse('get_all_songs')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.song1 = Song.objects.create(
            title='Song 1',
            singer='Singer 1',
            uploader=self.user,
            visible=True,
            cover=self.cover,
            audio=self.audio,
        )
        self.song2 = Song.objects.create(
            title='Song 2',
            singer='Singer 2',
            uploader=self.user,
            visible=False,
            cover=self.cover,
            audio=self.audio,
        )
        self.song3 = Song.objects.create(
            title='Song 3',
            singer='Singer 3',
            uploader=self.user,
            visible=True,
            cover=self.cover,
            audio=self.audio,
        )

    def test_get_all_songs_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取所有歌曲信息成功')
        self.assertEqual(response.json()['data'][-2:][0]['title'], 'Song 1')
        self.assertEqual(response.json()['data'][-2:][1]['title'], 'Song 3')

    def test_get_all_songs_no_visible_songs(self):
        self.song1.visible = False
        self.song1.save()
        self.song3.visible = False
        self.song3.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取所有歌曲信息成功')
        self.assertNotEqual(response.json()['data'][-2:][0]['title'], 'Song 1'),
        self.assertNotEqual(response.json()['data'][-2:][1]['title'], 'Song 2')

    def tearDown(self):
        self.user.delete()
        self.song1.delete()
        self.song2.delete()
        self.song3.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class QuerySongsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('query_songs')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.song1 = Song.objects.create(
            title='Song 1',
            singer='Singer 1',
            uploader=self.user,
            visible=True,
            cover='covers/test_cover1.jpg',
            audio='audios/test_audio1.mp3'
        )
        self.song2 = Song.objects.create(
            title='Song 2',
            singer='Singer 2',
            uploader=self.user,
            visible=False,
            cover='covers/test_cover2.jpg',
            audio='audios/test_audio2.mp3'
        )
        self.song3 = Song.objects.create(
            title='Song 3',
            singer='Singer 3',
            uploader=self.user,
            visible=True,
            cover='covers/test_cover3.jpg',
            audio='audios/test_audio3.mp3'
        )

    def test_query_songs_success(self):
        response = self.client.get(self.url, {'title': 'Song', 'singer': 'Singer 1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '搜索成功')
        self.assertEqual(len(response.json()['data']), 1)
        self.assertEqual(response.json()['data'][0]['title'], 'Song 1')

    def test_query_songs_no_results(self):
        response = self.client.get(self.url, {'title': 'Nonexistent Song'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '搜索成功')
        self.assertEqual(len(response.json()['data']), 0)

    def test_query_songs_no_search_keywords(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少搜索关键字'})

    def tearDown(self):
        self.user.delete()
        self.song1.delete()
        self.song2.delete()
        self.song3.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class GetCommentsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_comments')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.user,
            visible=True
        )
        self.comment1 = Comment.objects.create(
            user=self.user,
            song=self.song,
            content='Great song!',
            like=10
        )
        self.comment2 = Comment.objects.create(
            user=self.user,
            song=self.song,
            content='Nice beat!',
            like=5
        )

    def test_get_comments_success(self):
        response = self.client.get(self.url, {'songID': self.song.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取评论成功')
        self.assertEqual(len(response.json()['data']), 2)
        self.assertEqual(response.json()['data'][0]['content'], 'Great song!')
        self.assertEqual(response.json()['data'][1]['content'], 'Nice beat!')

    def test_get_comments_no_comments(self):
        another_song = Song.objects.create(
            title='Another Song',
            singer='Another Singer',
            uploader=self.user,
            visible=True
        )
        response = self.client.get(self.url, {'songID': another_song.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取评论成功')
        self.assertEqual(len(response.json()['data']), 0)

    def test_get_comments_invalid_songID(self):
        response = self.client.get(self.url, {'songID': 999})
        self.assertEqual(response.status_code, 200)  # 即使歌曲ID不存在，依然返回成功，只是数据为空
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取评论成功')
        self.assertEqual(len(response.json()['data']), 0)

    def tearDown(self):
        self.user.delete()
        self.song.delete()
        self.comment1.delete()
        self.comment2.delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)

class ComplainTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('complaint')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.another_user = User.objects.create(
            username='anotheruser',
            email='anotheruser@example.com',
            password='password'
        )
        self.admin_user = User.objects.get(username='yy')
        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.another_user,
            visible=True
        )
        self.songlist = SongList.objects.create(
            title='Test SongList',
            owner=self.another_user
        )
        self.token = generate_token('testuser', 'user')

    def test_complain_song_success(self):
        data = {
            'song_id': self.song.id,
            'content': 'This is a complaint about the song.'
        }
        response = self.client.post('/songs/complaint', data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.json()['message'], '投诉成功')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertTrue(Complaint.objects.filter(complainer=self.user, object_type='song', object_id=self.song.id).exists())

    def test_complain_songlist_success(self):
        data = {
            'songlist_id': self.songlist.id,
            'content': 'This is a complaint about the songlist.'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.json()['message'], '投诉成功')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertTrue(Complaint.objects.filter(complainer=self.user, object_type='songlist', object_id=self.songlist.id).exists())

    def test_complain_own_content(self):
        data = {
            'song_id': self.song.id,
            'content': 'This is a complaint about the song.'
        }
        self.song.uploader = self.user
        self.song.save()
        response = self.client.post('/songs/complaint', data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '不能投诉属于自己的内容')

    def test_complain_user_not_exist(self):
        data = {
            'song_id': self.song.id,
            'content': 'This is a complaint about the song.'
        }
        self.user.delete()
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '投诉者不存在')

    def test_complain_song_not_exist(self):
        data = {
            'song_id': 999,
            'content': 'This is a complaint about the song.'
        }
        response = self.client.post('/songs/complaint', data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '被投诉歌曲不存在')

    def test_complain_songlist_not_exist(self):
        data = {
            'songlist_id': 999,
            'content': 'This is a complaint about the songlist.'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '被投诉歌单不存在')

    def tearDown(self):
        self.song.delete()
        self.songlist.delete()
        Complaint.objects.all().delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)


class GetInitSingerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_init_singer')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.song1 = Song.objects.create(
            title='Song 1',
            singer='Singer1',
            uploader=self.user,
            cover='covers/test_cover1.jpg',
            audio='audios/test_audio1.mp3'
        )
        self.song2 = Song.objects.create(
            title='Song 2',
            singer='Singer2,Singer3',
            uploader=self.user,
            cover='covers/test_cover2.jpg',
            audio='audios/test_audio2.mp3'
        )
        self.token = generate_token('testuser', 'user')

    def test_get_init_singer_success(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True, 'message': '更新完成'})
        self.assertEqual(Singer.objects.filter(singerName='Singer1').count(), 1)
        self.assertEqual(Singer.objects.filter(singerName='Singer2').count(), 1)
        self.assertEqual(Singer.objects.filter(singerName='Singer3').count(), 1)

    def test_get_init_singer_delete_existing_singers(self):
        Singer.objects.create(singerName='ExistingSinger')
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True, 'message': '更新完成'})
        self.assertEqual(Singer.objects.filter(singerName='ExistingSinger').count(), 0)

    def test_get_init_singer_no_songs(self):
        Song.objects.all().delete()
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True, 'message': '更新完成'})
        self.assertEqual(Singer.objects.count(), 0)

    def test_get_init_singer_missing_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Authorization header missing'})

    def test_get_init_singer_invalid_token(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION='Bearer invalid_token')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Invalid token'})

    def tearDown(self):
        self.user.delete()
        Song.objects.all().delete()
        Singer.objects.all().delete()
        delete_files_except(cover_directory, exception_cover_file)
        delete_files_except(audio_directory, exception_audio_file)
