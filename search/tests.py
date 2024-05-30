import os
from unittest.mock import patch, mock_open
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.db.models import Q

from songlist.models import SongList
from user.models import User
from song.models import Song


class SearchSongsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.song1 = Song.objects.create(
            title='Happy Song',
            singer='Happy Singer',
            uploader=self.user,
            cover='covers/test_cover1.jpg',
            audio='audios/test_audio1.mp3',
            tag_theme='背景音乐',
            tag_scene='咖啡馆',
            tag_mood='开心',
            tag_style='民谣',
            tag_language='英语',
            visible=True
        )
        self.song2 = Song.objects.create(
            title='Sad Song',
            singer='Sad Singer',
            uploader=self.user,
            cover='covers/test_cover2.jpg',
            audio='audios/test_audio2.mp3',
            tag_theme='综艺',
            tag_scene='运动',
            tag_mood='伤感',
            tag_style='摇滚',
            tag_language='国语',
            visible=True
        )
        self.url = reverse('search_songs')

        # 创建必要的文件
        self.stopwords_path = '../stopwords.txt'
        self.stopwords_content = "a\nan\nthe\nand\n"

    @patch('builtins.open', new_callable=mock_open, read_data="a\nan\nthe\nand\n")
    @patch('search.views.jieba.cut_for_search')
    def test_search_songs_success(self, mock_jieba_cut_for_search, mock_open_file):
        mock_jieba_cut_for_search.side_effect = lambda keyword: keyword.split()
        response = self.client.get(self.url, {'keyword': 'sad', 'num': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '搜索成功')
        self.assertIn('data', response.json())
        songs_data = response.json()['data']
        self.assertEqual(len(songs_data), 1)
        self.assertEqual(songs_data[0]['title'], 'Sad Song')

    @patch('builtins.open', new_callable=mock_open, read_data="a\nan\nthe\nand\n")
    @patch('search.views.jieba.cut_for_search')
    def test_search_songs_stopwords_filtering(self, mock_jieba_cut_for_search, mock_open_file):
        mock_jieba_cut_for_search.side_effect = lambda keyword: keyword.split()
        response = self.client.get(self.url, {'keyword': 'a Happy the'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '搜索成功')
        self.assertIn('data', response.json())
        songs_data = response.json()['data']
        self.assertEqual(len(songs_data), 1)
        self.assertEqual(songs_data[0]['title'], 'Happy Song')

    @patch('builtins.open', new_callable=mock_open, read_data="a\nan\nthe\nand\n")
    @patch('search.views.jieba.cut_for_search')
    def test_search_songs_with_parameters(self, mock_jieba_cut_for_search, mock_open_file):
        mock_jieba_cut_for_search.side_effect = lambda keyword: keyword.split()
        response = self.client.get(self.url, {'tag_theme': '背景音乐', 'tag_scene': '咖啡馆'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '搜索成功')
        self.assertIn('data', response.json())
        songs_data = response.json()['data']
        self.assertEqual(len(songs_data), 1)
        self.assertEqual(songs_data[0]['title'], 'Happy Song')

    def tearDown(self):
        self.user.delete()
        self.song1.delete()
        self.song2.delete()


class SearchSonglistsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.songlist1 = SongList.objects.create(
            title='Happy Playlist',
            owner=self.user,
            cover='covers/test_cover1.jpg',
            tag_theme='情歌',
            tag_scene='睡前',
            tag_mood='甜蜜',
            tag_style='摇滚',
            tag_language='英语',
            visible=True
        )
        self.songlist2 = SongList.objects.create(
            title='Sad Playlist',
            owner=self.user,
            cover='covers/test_cover2.jpg',
            tag_theme='经典老歌',
            tag_scene='驾驶',
            tag_mood='伤感',
            tag_style='流行',
            tag_language='国语',
            visible=True
        )
        self.url = reverse('search_songlists')

    @patch('search.views.jieba.cut_for_search')
    def test_search_songlists_success(self, mock_jieba_cut_for_search):
        mock_jieba_cut_for_search.side_effect = lambda keyword: keyword.split()
        response = self.client.get(self.url, {'keyword': 'Happy', 'num': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '搜索成功')
        self.assertIn('data', response.json())
        songlists_data = response.json()['data']
        self.assertEqual(len(songlists_data), 1)
        self.assertEqual(songlists_data[0]['title'], 'Happy Playlist')

    @patch('search.views.jieba.cut_for_search')
    def test_search_songlists_with_parameters(self, mock_jieba_cut_for_search):
        mock_jieba_cut_for_search.side_effect = lambda keyword: keyword.split()
        response = self.client.get(self.url, {'tag_theme': '情歌', 'tag_scene': '睡前'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '搜索成功')
        self.assertIn('data', response.json())
        songlists_data = response.json()['data']
        self.assertEqual(len(songlists_data), 1)
        self.assertEqual(songlists_data[0]['title'], 'Happy Playlist')

    def tearDown(self):
        self.user.delete()
        self.songlist1.delete()
        self.songlist2.delete()


class SearchUsersTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(
            username='happyuser',
            email='happyuser@example.com',
            password='password'
        )
        self.user2 = User.objects.create(
            username='saduser',
            email='saduser@example.com',
            password='password'
        )
        self.url = reverse('search_users')

    @patch('search.views.jieba.cut_for_search')
    def test_search_users_success(self, mock_jieba_cut_for_search):
        mock_jieba_cut_for_search.side_effect = lambda keyword: keyword.split()
        response = self.client.get(self.url, {'keyword': 'happy', 'num': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '搜索成功')
        self.assertIn('data', response.json())
        users_data = response.json()['data']
        self.assertEqual(len(users_data), 1)
        self.assertEqual(users_data[0]['username'], 'happyuser')

    @patch('search.views.jieba.cut_for_search')
    def test_search_users_with_parameters(self, mock_jieba_cut_for_search):
        mock_jieba_cut_for_search.side_effect = lambda keyword: keyword.split()
        response = self.client.get(self.url, {'keyword': 'happy'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '搜索成功')
        self.assertIn('data', response.json())
        users_data = response.json()['data']
        self.assertEqual(len(users_data), 1)
        self.assertEqual(users_data[0]['username'], 'happyuser')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
