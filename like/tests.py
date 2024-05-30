from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from user.models import User
from songlist.models import SongList
from .models import LikedSongList
from django.http import JsonResponse, request
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from user.tests import generate_token

from songlist.models import SongList
from user.models import User
from song.models import Song
from .models import LikedSong, LikedSongList
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from user.tests import generate_token


# class LikedSongsGetTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             username='testuser',
#             email='testuser@example.com',
#             password='password',
#             permission_liked_songs=True
#         )
#         self.admin_user = User.objects.create(
#             username='admin',
#             email='admin@example.com',
#             password='password',
#             role='admin'
#         )
#         self.other_user = User.objects.create(
#             username='otheruser',
#             email='otheruser@example.com',
#             password='password',
#             permission_liked_songs=False
#         )
#         self.song1 = Song.objects.create(
#             title='Song 1',
#             singer='Singer 1',
#             cover='cover1.jpg',
#             audio='audio1.mp3',
#             uploader_id=self.user.user_id,
#             visible=True
#         )
#         self.song2 = Song.objects.create(
#             title='Song 2',
#             singer='Singer 2',
#             cover='cover2.jpg',
#             audio='audio2.mp3',
#             uploader_id=self.user.user_id,
#             visible=True
#         )
#         LikedSong.objects.create(user=self.user, song=self.song1)
#         LikedSong.objects.create(user=self.user, song=self.song2)
#
#         self.url = reverse('liked_songs_get')
#         self.token = generate_token(self.user.username, self.user.role)
#         self.admin_token = generate_token(self.admin_user.username, self.admin_user.role)
#         self.other_token = generate_token(self.other_user.username, self.other_user.role)
#
#     def test_liked_songs_get_success(self):
#         response = self.client.get(self.url, {'username': self.user.username}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['success'], True)
#         self.assertEqual(response.json()['message'], '获取用户喜欢歌曲成功')
#         self.assertIn('data', response.json())
#         songs_data = response.json()['data']
#         self.assertEqual(len(songs_data), 2)
#
#     def test_liked_songs_get_no_username(self):
#         response = self.client.get(self.url, {}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '未获取到用户名')
#
#     def test_liked_songs_get_user_not_exist(self):
#         response = self.client.get(self.url, {'username': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '用户不存在')
#
#     def test_liked_songs_get_private_user_not_admin_or_owner(self):
#         response = self.client.get(self.url, {'username': self.other_user.username}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 403)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '获取失败，用户设置为隐私')
#
#     def test_liked_songs_get_private_user_admin(self):
#         response = self.client.get(self.url, {'username': self.other_user.username}, HTTP_AUTHORIZATION=self.admin_token)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['success'], True)
#         self.assertEqual(response.json()['message'], '获取用户喜欢歌曲成功')
#         self.assertIn('data', response.json())
#
#     def tearDown(self):
#         self.user.delete()
#         self.admin_user.delete()
#         self.other_user.delete()
#         self.song1.delete()
#         self.song2.delete()


# class LikedSongsAddTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             username='testuser',
#             email='testuser@example.com',
#             password='password'
#         )
#         self.song = Song.objects.create(
#             title='Song 1',
#             singer='Singer 1',
#             cover='cover1.jpg',
#             audio='audio1.mp3',
#             uploader_id=self.user.user_id,
#             visible=True
#         )
#         self.url = reverse('liked_songs_add')
#         self.token = generate_token(self.user.username, self.user.role)
#
#     def test_liked_songs_add_success(self):
#         response = self.client.post(self.url, {'song_id': self.song.id}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json()['success'], True)
#         self.assertEqual(response.json()['message'], '歌曲已添加到喜爱列表')
#         self.assertTrue(LikedSong.objects.filter(user=self.user, song=self.song).exists())
#         self.song.refresh_from_db()
#         self.assertEqual(self.song.like, 1)
#
#     def test_liked_songs_add_already_liked(self):
#         LikedSong.objects.create(user=self.user, song=self.song)
#         response = self.client.post(self.url, {'song_id': self.song.id}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json()['success'], True)
#         self.assertEqual(response.json()['message'], '歌曲已在喜爱列表中')
#         self.assertTrue(LikedSong.objects.filter(user=self.user, song=self.song).exists())
#         self.song.refresh_from_db()
#         self.assertEqual(self.song.like, 0)  # 因为没有增加新的点赞
#
#     def test_liked_songs_add_no_song_id(self):
#         response = self.client.post(self.url, {}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '未获取到歌曲id')
#
#     def test_liked_songs_add_no_username(self):
#         invalid_token = generate_token('', self.user.role)  # 生成一个没有用户名的token
#         response = self.client.post(self.url, {'song_id': self.song.id}, HTTP_AUTHORIZATION=invalid_token)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '未获取到用户名')
#
#     def test_liked_songs_add_user_not_exist(self):
#         invalid_token = generate_token('nonexistentuser', self.user.role)
#         response = self.client.post(self.url, {'song_id': self.song.id}, HTTP_AUTHORIZATION=invalid_token)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '用户不存在')
#
#     def test_liked_songs_add_song_not_exist(self):
#         response = self.client.post(self.url, {'song_id': 99999}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '歌曲不存在')
#
#     def tearDown(self):
#         self.user.delete()
#         self.song.delete()


# class LikedSongsDeleteTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             username='testuser',
#             email='testuser@example.com',
#             password='password'
#         )
#         self.song = Song.objects.create(
#             title='Song 1',
#             singer='Singer 1',
#             cover='cover1.jpg',
#             audio='audio1.mp3',
#             uploader_id=self.user.user_id,
#             visible=True
#         )
#         self.liked_song = LikedSong.objects.create(user=self.user, song=self.song)
#         self.url = reverse('liked_songs_delete')
#         self.token = generate_token(self.user.username, self.user.role)
#
#     def test_liked_songs_delete_success(self):
#         response = self.client.post(self.url, {'song_id': self.song.id}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['success'], True)
#         self.assertEqual(response.json()['message'], '歌曲已从喜爱列表中移除')
#         self.assertFalse(LikedSong.objects.filter(user=self.user, song=self.song).exists())
#         self.song.refresh_from_db()
#         self.assertEqual(self.song.like, 0)
#
#     def test_liked_songs_delete_no_song_id(self):
#         response = self.client.post(self.url, {}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '未获取到歌曲id')
#
#     def test_liked_songs_delete_no_username(self):
#         invalid_token = generate_token('', self.user.role)  # 生成一个没有用户名的token
#         response = self.client.post(self.url, {'song_id': self.song.id}, HTTP_AUTHORIZATION=invalid_token)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '未获取到用户名')
#
#     def test_liked_songs_delete_user_not_exist(self):
#         invalid_token = generate_token('nonexistentuser', self.user.role)
#         response = self.client.post(self.url, {'song_id': self.song.id}, HTTP_AUTHORIZATION=invalid_token)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '用户不存在')
#
#     def test_liked_songs_delete_song_not_exist(self):
#         response = self.client.post(self.url, {'song_id': 99999}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '歌曲不存在')
#
#     def test_liked_songs_delete_liked_song_not_exist(self):
#         self.liked_song.delete()
#         response = self.client.post(self.url, {'song_id': self.song.id}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '喜爱歌曲列表不存在')
#
#     def tearDown(self):
#         self.user.delete()
#         self.song.delete()


# class LikedSongListsGetTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             username='testuser',
#             email='testuser@example.com',
#             password='password'
#         )
#         self.songlist1 = SongList.objects.create(
#             title='SongList 1',
#             cover='cover1.jpg',
#             owner=self.user,
#             visible=True
#         )
#         self.songlist2 = SongList.objects.create(
#             title='SongList 2',
#             cover='cover2.jpg',
#             owner=self.user,
#             visible=True
#         )
#         self.liked_songlist1 = LikedSongList.objects.create(user=self.user, songlist=self.songlist1)
#         self.liked_songlist2 = LikedSongList.objects.create(user=self.user, songlist=self.songlist2)
#         self.url = reverse('liked_songlists_get')
#         self.token = generate_token(self.user.username, self.user.role)
#
#     def test_liked_songlists_get_success(self):
#         response = self.client.get(self.url, {'username': self.user.username}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['success'], True)
#         self.assertEqual(response.json()['message'], '获取用户喜欢歌单成功')
#         self.assertIn('data', response.json())
#         songlists_data = response.json()['data']
#         self.assertEqual(len(songlists_data), 2)
#
#     def test_liked_songlists_get_no_username(self):
#         response = self.client.get(self.url, {}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '未获取到用户名')
#
#     def test_liked_songlists_get_user_not_exist(self):
#         response = self.client.get(self.url, {'username': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '用户不存在')
#
#     def tearDown(self):
#         self.user.delete()
#         self.songlist1.delete()
#         self.songlist2.delete()


# class LikedSongListsAddTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             username='testuser',
#             email='testuser@example.com',
#             password='password'
#         )
#         self.songlist = SongList.objects.create(
#             title='SongList 1',
#             cover='cover1.jpg',
#             owner=self.user,
#             visible=True
#         )
#         self.url = reverse('liked_songlists_add')
#         self.token = generate_token(self.user.username, self.user.role)
#
#     def test_liked_songlists_add_success(self):
#         response = self.client.post(self.url, {'songlist_id': self.songlist.id}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json()['success'], True)
#         self.assertEqual(response.json()['message'], '歌单已添加到喜爱列表')
#         self.assertTrue(LikedSongList.objects.filter(user=self.user, songlist=self.songlist).exists())
#         self.songlist.refresh_from_db()
#         self.assertEqual(self.songlist.like, 1)
#
#     def test_liked_songlists_add_already_liked(self):
#         LikedSongList.objects.create(user=self.user, songlist=self.songlist)
#         response = self.client.post(self.url, {'songlist_id': self.songlist.id}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json()['success'], True)
#         self.assertEqual(response.json()['message'], '歌单已在喜爱列表中')
#         self.assertTrue(LikedSongList.objects.filter(user=self.user, songlist=self.songlist).exists())
#         self.songlist.refresh_from_db()
#         self.assertEqual(self.songlist.like, 0)  # 因为没有增加新的点赞
#
#     def test_liked_songlists_add_no_songlist_id(self):
#         response = self.client.post(self.url, {}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '未获取到歌单id')
#
#     def test_liked_songlists_add_no_username(self):
#         invalid_token = generate_token('', self.user.role)  # 生成一个没有用户名的token
#         response = self.client.post(self.url, {'songlist_id': self.songlist.id}, HTTP_AUTHORIZATION=invalid_token)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '未获取到用户名')
#
#     def test_liked_songlists_add_user_not_exist(self):
#         invalid_token = generate_token('nonexistentuser', self.user.role)
#         response = self.client.post(self.url, {'songlist_id': self.songlist.id}, HTTP_AUTHORIZATION=invalid_token)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '用户不存在')
#
#     def test_liked_songlists_add_songlist_not_exist(self):
#         response = self.client.post(self.url, {'songlist_id': 99999}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json()['success'], False)
#         self.assertEqual(response.json()['message'], '歌单不存在')
#
#     def tearDown(self):
#         self.user.delete()
#         self.songlist.delete()


class LikedSongListsDeleteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.songlist = SongList.objects.create(
            title='SongList 1',
            cover='cover1.jpg',
            owner=self.user,
            visible=True
        )
        self.liked_songlist = LikedSongList.objects.create(user=self.user, songlist=self.songlist)
        self.url = reverse('liked_songlists_delete')
        self.token = generate_token(self.user.username, self.user.role)

    def test_liked_songlists_delete_success(self):
        response = self.client.post(self.url, {'songlist_id': self.songlist.id}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '歌单已从喜爱列表中移除')
        self.assertFalse(LikedSongList.objects.filter(user=self.user, songlist=self.songlist).exists())
        self.songlist.refresh_from_db()
        self.assertEqual(self.songlist.like, 0)

    def test_liked_songlists_delete_no_songlist_id(self):
        response = self.client.post(self.url, {}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '未获取到歌单id')

    def test_liked_songlists_delete_no_username(self):
        invalid_token = generate_token('', self.user.role)  # 生成一个没有用户名的token
        response = self.client.post(self.url, {'songlist_id': self.songlist.id}, HTTP_AUTHORIZATION=invalid_token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '未获取到用户名')

    def test_liked_songlists_delete_user_not_exist(self):
        invalid_token = generate_token('nonexistentuser', self.user.role)
        response = self.client.post(self.url, {'songlist_id': self.songlist.id}, HTTP_AUTHORIZATION=invalid_token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '用户不存在')

    def test_liked_songlists_delete_songlist_not_exist(self):
        response = self.client.post(self.url, {'songlist_id': 99999}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '歌单不存在')

    def test_liked_songlists_delete_liked_songlist_not_exist(self):
        self.liked_songlist.delete()
        response = self.client.post(self.url, {'songlist_id': self.songlist.id}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '喜爱歌单列表不存在')

    def tearDown(self):
        self.user.delete()
        self.songlist.delete()