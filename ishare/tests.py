import json
import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch, MagicMock

from like.models import LikedSongList
from songlist.models import SongList
from user.models import User
from message.models import Message
from ishare.models import Ishare, ShareSongs
from user.tests import generate_token


class ShareLikedSongsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.friend = User.objects.create(
            username='frienduser',
            email='frienduser@example.com',
            password='password'
        )
        self.token = generate_token(self.user.username, self.user.role)
        self.url = reverse('share_liked_songs')

    @patch('ishare.views.send_message')
    def test_share_to_friend_success(self, mock_send_message):
        mock_send_message.return_value = (True, 123)
        data = {
            'type': '1',
            'friend': 'frienduser'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '分享给好友成功')
        self.assertTrue(Ishare.objects.filter(creator=self.user, s_type=0, content='123').exists())

    def test_generate_share_code_success(self):
        data = {
            'type': '2'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '生成分享码成功')
        self.assertIn('data', response.json())
        self.assertTrue(Ishare.objects.filter(creator=self.user, s_type=1).exists())

    def test_user_does_not_exist(self):
        invalid_token = generate_token('invaliduser', 'user')
        data = {
            'type': '1',
            'friend': 'frienduser'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=invalid_token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '用户不存在')

    def test_general_exception(self):
        with patch('ishare.views.User.objects.get') as mock_get_user:
            mock_get_user.side_effect = Exception('Some error')
            data = {
                'type': '1',
                'friend': 'frienduser'
            }
            response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json()['success'], False)
            self.assertEqual(response.json()['message'], 'Some error')

    def tearDown(self):
        self.user.delete()
        self.friend.delete()


class ShareSonglistTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.friend = User.objects.create(
            username='frienduser',
            email='frienduser@example.com',
            password='password'
        )
        self.songlist = SongList.objects.create(
            title='Test SongList',
            cover='covers/test_cover.jpg',
            owner=self.user,
            visible=True
        )
        self.token = generate_token(self.user.username, self.user.role)
        self.url = reverse('share_songlist')

    @patch('ishare.views.send_message')
    def test_share_songlist_to_friend_success(self, mock_send_message):
        mock_send_message.return_value = (True, 123)
        data = {
            'type': '1',
            'friend': 'frienduser',
            'songlist_id': self.songlist.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '分享给好友成功')
        self.assertTrue(Ishare.objects.filter(creator=self.user, s_type=0, content='123', obj_type=1, object_id=self.songlist.id).exists())

    def test_generate_share_code_for_songlist_success(self):
        data = {
            'type': '2',
            'songlist_id': self.songlist.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '生成分享码成功')
        self.assertIn('data', response.json())
        self.assertTrue(Ishare.objects.filter(creator=self.user, s_type=1, obj_type=1, object_id=self.songlist.id).exists())

    def test_user_does_not_exist(self):
        invalid_token = generate_token('invaliduser', 'user')
        data = {
            'type': '1',
            'friend': 'frienduser',
            'songlist_id': self.songlist.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=invalid_token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '用户不存在')

    def test_songlist_does_not_exist(self):
        data = {
            'type': '1',
            'friend': 'frienduser',
            'songlist_id': 999
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.json()['message'], '歌单不存在')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)

    def test_general_exception(self):
        with patch('ishare.views.User.objects.get') as mock_get_user:
            mock_get_user.side_effect = Exception('Some error')
            data = {
                'type': '1',
                'friend': 'frienduser',
                'songlist_id': self.songlist.id
            }
            response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json()['success'], False)
            self.assertEqual(response.json()['message'], 'Some error')

    def tearDown(self):
        self.user.delete()
        self.friend.delete()
        self.songlist.delete()


class HandleShareTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.creator = User.objects.create(
            username='creatoruser',
            email='creatoruser@example.com',
            password='password'
        )
        self.songlist = SongList.objects.create(
            title='Test SongList',
            cover='covers/test_cover.jpg',
            owner=self.creator,
            visible=True
        )
        self.expired_date = datetime.datetime.now() - datetime.timedelta(days=1)
        self.valid_date = datetime.datetime.now() + datetime.timedelta(days=1)

        self.ishare_message = Ishare.objects.create(
            creator=self.creator,
            s_type=0,
            content='123',
            obj_type=0,
            expire_date=self.valid_date
        )

        self.ishare_code = Ishare.objects.create(
            creator=self.creator,
            s_type=1,
            content='abc',
            obj_type=1,
            object_id=self.songlist.id,
            expire_date=self.valid_date
        )

        self.expired_ishare = Ishare.objects.create(
            creator=self.creator,
            s_type=1,
            content='expired',
            obj_type=1,
            object_id=self.songlist.id,
            expire_date=self.expired_date
        )

        self.token = generate_token(self.user.username, self.user.role)
        self.url = reverse('handle_share')

    def test_handle_share_with_message_id_success(self):
        data = {
            'message_id': '123'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '接受分享成功')
        self.assertTrue(ShareSongs.objects.filter(user=self.user, shared_user=self.creator).exists())

    def test_handle_share_with_code_success(self):
        data = {
            'code': 'abc'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '接受分享成功，歌单已添加到收藏夹')
        self.assertTrue(LikedSongList.objects.filter(user=self.user, songlist=self.songlist).exists())

    def test_handle_share_with_code_already_in_list(self):
        LikedSongList.objects.create(user=self.user, songlist=self.songlist)
        data = {
            'code': 'abc'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '歌单已在收藏列表中')

    def test_handle_share_with_expired_code(self):
        data = {
            'code': 'expired'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '分享码不存在或已失效')

    def test_handle_share_with_missing_params(self):
        data = {}
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '参数不足')

    def test_user_does_not_exist(self):
        invalid_token = generate_token('invaliduser', 'user')
        data = {
            'code': 'abc'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=invalid_token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '用户不存在')

    def test_ishare_does_not_exist(self):
        data = {
            'message_id': 'nonexistent'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '分享记录不存在')

    def test_songlist_does_not_exist(self):
        invalid_ishare = Ishare.objects.create(
            creator=self.creator,
            s_type=1,
            content='invalidsonglist',
            obj_type=1,
            object_id=9999,
            expire_date=self.valid_date
        )
        data = {
            'code': 'invalidsonglist'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '歌单不存在')

    def test_general_exception(self):
        with patch('ishare.views.User.objects.get') as mock_get_user:
            mock_get_user.side_effect = Exception('Some error')
            data = {
                'code': 'abc'
            }
            response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json()['success'], False)
            self.assertEqual(response.json()['message'], 'Some error')

    def tearDown(self):
        self.user.delete()
        self.creator.delete()
        self.songlist.delete()
        self.ishare_message.delete()
        self.ishare_code.delete()
        self.expired_ishare.delete()