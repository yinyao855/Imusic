from django.test import TestCase, Client
from django.urls import reverse

from singer.models import Singer
from songlist.models import SongList
from user.models import User  # 确保导入的是我们定义的User模型
from song.models import Song
from feature.models import Recent
from user.tests import generate_token


# class GetRecentTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             username='testuser',
#             role='user',
#             email='testuser@example.com',
#             password='password'
#         )
#         self.song1 = Song.objects.create(
#             title='Song 1',
#             singer='Singer 1',
#             uploader=self.user,
#             cover='covers/test_cover1.jpg',
#             audio='audios/test_audio1.mp3',
#             visible=True
#         )
#         self.song2 = Song.objects.create(
#             title='Song 2',
#             singer='Singer 2',
#             uploader=self.user,
#             cover='covers/test_cover2.jpg',
#             audio='audios/test_audio2.mp3',
#             visible=True
#         )
#         self.song3 = Song.objects.create(
#             title='Song 3',
#             singer='Singer 3',
#             uploader=self.user,
#             cover='covers/test_cover3.jpg',
#             audio='audios/test_audio3.mp3',
#             visible=True
#         )
#         self.recent1 = Recent.objects.create(
#             user=self.user,
#             song=self.song1,
#             play_count=10
#         )
#         self.recent2 = Recent.objects.create(
#             user=self.user,
#             song=self.song2,
#             play_count=5
#         )
#         self.recent3 = Recent.objects.create(
#             user=self.user,
#             song=self.song3,
#             play_count=3
#         )
#         self.url = reverse('recent')
#         self.token = generate_token(self.user.username, self.user.role)
#
#     def test_get_recent_songs_success(self):
#         response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         response_data = response.json()
#         self.assertTrue(response_data['success'])
#         self.assertEqual(response_data['message'], '查询最近播放歌曲成功')
#         self.assertIn('data', response_data)
#         self.assertEqual(len(response_data['data']['songs']), 3)
#
#     def test_get_recent_songs_with_num_parameter(self):
#         response = self.client.get(self.url, {'num': '2'}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         response_data = response.json()
#         self.assertTrue(response_data['success'])
#         self.assertEqual(response_data['message'], '查询最近播放歌曲成功')
#         self.assertEqual(len(response_data['data']['songs']), 2)
#
#     def test_get_recent_songs_with_invalid_num_parameter(self):
#         response = self.client.get(self.url, {'num': 'invalid'}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 500)
#         response_data = response.json()
#         self.assertFalse(response_data['success'])
#
#     def tearDown(self):
#         self.user.delete()
#         self.song1.delete()
#         self.song2.delete()
#         self.song3.delete()
#         self.recent1.delete()
#         self.recent2.delete()
#         self.recent3.delete()


# class AddRecentTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             username='testuser',
#             email='testuser@example.com',
#             password='password'
#         )
#         self.song1 = Song.objects.create(
#             title='Song 1',
#             singer='Singer 1',
#             uploader=self.user,
#             cover='covers/test_cover1.jpg',
#             audio='audios/test_audio1.mp3',
#             visible=True
#         )
#         self.song2 = Song.objects.create(
#             title='Song 2',
#             singer='Singer 2',
#             uploader=self.user,
#             cover='covers/test_cover2.jpg',
#             audio='audios/test_audio2.mp3',
#             visible=True
#         )
#         self.url = reverse('add')
#         self.token = generate_token(self.user.username, self.user.role)
#
#     def test_add_recent_song_success_new_entry(self):
#         data = {'song_id': self.song1.id}
#         response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         response_data = response.json()
#         self.assertTrue(response_data['success'])
#         self.assertEqual(response_data['message'], '添加最近播放成功')
#         recent = Recent.objects.get(user=self.user, song=self.song1)
#         self.assertEqual(recent.play_count, 1)
#         self.assertEqual(recent.w_play_count, 1)
#
#     def test_add_recent_song_success_existing_entry(self):
#         from django.utils import timezone
#         Recent.objects.create(user=self.user, song=self.song1, play_count=5, w_play_count=5, last_play=timezone.now())
#         data = {'song_id': self.song1.id}
#         response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         response_data = response.json()
#         self.assertTrue(response_data['success'])
#         self.assertEqual(response_data['message'], '添加最近播放成功')
#         recent = Recent.objects.get(user=self.user, song=self.song1)
#         self.assertEqual(recent.play_count, 6)
#         self.assertEqual(recent.w_play_count, 6)
#
#     def test_add_recent_song_missing_song_id(self):
#         data = {}
#         response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
#         response_data = response.json()
#         self.assertEqual(response_data['message'], '未接收到用户姓名或歌曲id')
#         self.assertEqual(response.status_code, 400)
#         self.assertFalse(response_data['success'])
#
#     def tearDown(self):
#         self.user.delete()
#         self.song1.delete()
#         self.song2.delete()


# class GetHotSongListsTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             username='testuser',
#             email='testuser@example.com',
#             password='password'
#         )
#         self.song1 = Song.objects.create(
#             title='Song 1',
#             singer='Singer 1',
#             uploader=self.user,
#             cover='covers/test_cover1.jpg',
#             audio='audios/test_audio1.mp3',
#             visible=True
#         )
#         self.song2 = Song.objects.create(
#             title='Song 2',
#             singer='Singer 2',
#             uploader=self.user,
#             cover='covers/test_cover2.jpg',
#             audio='audios/test_audio2.mp3',
#             visible=True
#         )
#         self.songlist1 = SongList.objects.create(
#             title='SongList 1',
#             owner=self.user,
#             cover='covers/test_cover1.jpg',
#             like=100,
#             visible=True
#         )
#         self.songlist2 = SongList.objects.create(
#             title='SongList 2',
#             owner=self.user,
#             cover='covers/test_cover2.jpg',
#             like=50,
#             visible=True
#         )
#         self.songlist3 = SongList.objects.create(
#             title='SongList 3',
#             owner=self.user,
#             cover='covers/test_cover3.jpg',
#             like=10,
#             visible=True
#         )
#         self.url = reverse('hot-song-lists')
#         self.token = generate_token(self.user.username, self.user.role)
#
#     def test_get_hot_songlists_success(self):
#         response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         response_data = response.json()
#         self.assertTrue(response_data['success'])
#         self.assertEqual(response_data['message'], '获取成功')
#         self.assertIn('data', response_data)
#
#     def test_get_hot_songlists_with_num_parameter(self):
#         response = self.client.get(self.url, {'num': '2'}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         response_data = response.json()
#         self.assertTrue(response_data['success'])
#         self.assertEqual(response_data['message'], '获取成功')
#         self.assertEqual(len(response_data['data']), 2)
#
#     def tearDown(self):
#         self.user.delete()
#         self.song1.delete()
#         self.song2.delete()
#         self.songlist1.delete()
#         self.songlist2.delete()
#         self.songlist3.delete()


# class GetHotSongsTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             username='testuser',
#             email='testuser@example.com',
#             password='password'
#         )
#         self.song1 = Song.objects.create(
#             title='Song 1',
#             singer='Singer 1',
#             uploader=self.user,
#             cover='covers/test_cover1.jpg',
#             audio='audios/test_audio1.mp3',
#             visible=True,
#             like=100
#         )
#         self.song2 = Song.objects.create(
#             title='Song 2',
#             singer='Singer 2',
#             uploader=self.user,
#             cover='covers/test_cover2.jpg',
#             audio='audios/test_audio2.mp3',
#             visible=True,
#             like=50
#         )
#         self.song3 = Song.objects.create(
#             title='Song 3',
#             singer='Singer 3',
#             uploader=self.user,
#             cover='covers/test_cover3.jpg',
#             audio='audios/test_audio3.mp3',
#             visible=True,
#             like=10
#         )
#         self.url = reverse('hot-songs')
#         self.token = generate_token(self.user.username, self.user.role)
#
#     def test_get_hot_songs_success(self):
#         response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         response_data = response.json()
#         self.assertTrue(response_data['success'])
#         self.assertEqual(response_data['message'], '获取成功')
#         self.assertIn('data', response_data)
#
#     def test_get_hot_songs_with_num_parameter(self):
#         response = self.client.get(self.url, {'num': '2'}, HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 200)
#         response_data = response.json()
#         self.assertTrue(response_data['success'])
#         self.assertEqual(response_data['message'], '获取成功')
#         self.assertEqual(len(response_data['data']), 2)
#
#     def tearDown(self):
#         self.user.delete()
#         self.song1.delete()
#         self.song2.delete()
#         self.song3.delete()


class HotSingersTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.song1 = Song.objects.create(
            title='Song 1',
            singer='Singer 1',
            uploader=self.user,
            cover='covers/test_cover1.jpg',
            audio='audios/test_audio1.mp3',
            visible=True
        )
        self.singer1 = Singer.objects.create(
            singerName='Singer 1',
            singerImage='singers/singer1.jpg'
        )
        self.singer2 = Singer.objects.create(
            singerName='Singer 2',
            singerImage='singers/singer2.jpg'
        )
        self.singer3 = Singer.objects.create(
            singerName='Singer 3'
        )
        self.singer1.songs.add(self.song1)
        self.url = reverse('hot-singers')
        self.token = generate_token(self.user.username, self.user.role)

    def test_get_hot_singers_success(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertIn('data', response_data)
        # self.assertEqual(len(response_data['data']), 2)  # 因为singer3没有singerImage

    def test_get_hot_singers_with_no_singer_image(self):
        response = self.client.get(self.url, {'num': '10'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        # self.assertEqual(len(response_data['data']), 2)  # 因为singer3没有singerImage

    def tearDown(self):
        self.user.delete()
        self.song1.delete()
        self.singer1.delete()
        self.singer2.delete()
        self.singer3.delete()