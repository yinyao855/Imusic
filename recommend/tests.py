import os
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from django.conf import settings

from like.models import LikedSong
from user.models import User
from song.models import Song
from user.tests import generate_token


class GetRecentSongsTests(TestCase):
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
            upload_date='2023-01-01 00:00:00',
            visible=True
        )
        self.song2 = Song.objects.create(
            title='Song 2',
            singer='Singer 2',
            uploader=self.user,
            cover='covers/test_cover2.jpg',
            audio='audios/test_audio2.mp3',
            upload_date='2023-01-02 00:00:00',
            visible=True
        )
        self.song3 = Song.objects.create(
            title='Song 3',
            singer='Singer 3',
            uploader=self.user,
            cover='covers/test_cover3.jpg',
            audio='audios/test_audio3.mp3',
            upload_date='2023-01-03 00:00:00',
            visible=True
        )
        self.url = reverse('latest')

    def test_get_recent_songs_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取最近歌曲成功')
        self.assertIn('data', response.json())
        songs_data = response.json()['data']
        self.assertEqual(len(songs_data), 15)
        self.assertEqual(songs_data[:3][0]['title'], 'Song 3')
        self.assertEqual(songs_data[:3][1]['title'], 'Song 2')
        self.assertEqual(songs_data[:3][2]['title'], 'Song 1')

    def test_get_recent_songs_with_num_parameter(self):
        response = self.client.get(self.url, {'num': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取最近歌曲成功')
        self.assertIn('data', response.json())
        songs_data = response.json()['data']
        self.assertEqual(len(songs_data), 2)
        self.assertEqual(songs_data[0]['title'], 'Song 3')
        self.assertEqual(songs_data[1]['title'], 'Song 2')

    def tearDown(self):
        self.user.delete()
        self.song1.delete()
        self.song2.delete()
        self.song3.delete()


class GetRecommendedSongsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            role='user',
            email='testuser@example.com',
            password='password'
        )
        self.another_user = User.objects.create(
            username='anotheruser',
            role='user',
            email='anotheruser@example.com',
            password='password'
        )
        self.song1 = Song.objects.create(
            title='Song 1',
            singer='Singer 1',
            uploader=self.another_user,
            cover='covers/test_cover1.jpg',
            audio='audios/test_audio1.mp3',
            tag_theme='Happy',
            tag_scene='Party',
            tag_mood='Joyful',
            tag_style='Pop',
            tag_language='English',
            upload_date='2023-01-01 00:00:00',
            visible=True
        )
        self.song2 = Song.objects.create(
            title='Song 2',
            singer='Singer 2',
            uploader=self.another_user,
            cover='covers/test_cover2.jpg',
            audio='audios/test_audio2.mp3',
            tag_theme='Sad',
            tag_scene='Alone',
            tag_mood='Melancholy',
            tag_style='Ballad',
            tag_language='English',
            upload_date='2023-01-02 00:00:00',
            visible=True
        )
        self.song3 = Song.objects.create(
            title='Song 3',
            singer='Singer 3',
            uploader=self.another_user,
            cover='covers/test_cover3.jpg',
            audio='audios/test_audio3.mp3',
            tag_theme='Relax',
            tag_scene='Chill',
            tag_mood='Calm',
            tag_style='Ambient',
            tag_language='English',
            upload_date='2023-01-03 00:00:00',
            visible=True
        )
        LikedSong.objects.create(user=self.user, song=self.song1)

        self.url = reverse('recommend')
        self.token = generate_token(self.user.username, self.user.role)

    def test_get_recommended_songs_success(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token,)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取推荐歌曲成功')
        self.assertIn('data', response.json())
        recommended_data = response.json()['data']
        self.assertGreaterEqual(len(recommended_data), 1)

    def tearDown(self):
        self.user.delete()
        self.another_user.delete()
        self.song1.delete()
        self.song2.delete()
        self.song3.delete()