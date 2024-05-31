from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse

from message.models import Message
from songlist.models import SongList
from user.models import User
from song.models import Song
from user.tests import generate_token
from .models import Complaint


class HandleComplaintTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('handle_complaint')
        self.admin_user = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.normal_user = User.objects.create(
            username='normaluser',
            email='normaluser@example.com',
            password='password',
            role='user'
        )
        self.complainer = User.objects.create(
            username='complainer',
            email='complainer@example.com',
            password='password'
        )
        self.complained = User.objects.create(
            username='complained',
            email='complained@example.com',
            password='password'
        )
        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.complained,
            visible=True
        )
        self.songlist = SongList.objects.create(
            title='Test SongList',
            owner=self.complained
        )
        self.complaint_song = Complaint.objects.create(
            complainer=self.complainer,
            complained=self.complained,
            content='Test complaint content',
            object_type='song',
            object_id=self.song.id
        )
        self.complaint_songlist = Complaint.objects.create(
            complainer=self.complainer,
            complained=self.complained,
            content='Test complaint content',
            object_type='songlist',
            object_id=self.songlist.id
        )
        self.token = generate_token('adminuser', 'admin')

    def test_handle_complaint_success_remove_song(self):
        data = {
            'complaint_id': self.complaint_song.id,
            'is_remove': 'true',
            'reason': 'Violation of terms'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '处理投诉成功')
        self.song.refresh_from_db()
        self.assertFalse(self.song.visible)

    def test_handle_complaint_success_keep_song(self):
        data = {
            'complaint_id': self.complaint_song.id,
            'is_remove': 'false',
            'reason': 'Not a valid complaint'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '处理投诉成功')
        self.song.refresh_from_db()
        self.assertTrue(self.song.visible)

    def test_handle_complaint_success_remove_songlist(self):
        data = {
            'complaint_id': self.complaint_songlist.id,
            'is_remove': 'true',
            'reason': 'Inappropriate content'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '处理投诉成功')
        self.songlist.refresh_from_db()
        self.assertFalse(self.songlist.visible)

    def test_handle_complaint_no_permission(self):
        self.token = generate_token('normaluser', 'user')
        data = {
            'complaint_id': self.complaint_song.id,
            'is_remove': 'true',
            'reason': 'Violation of terms'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '没有权限访问')

    def test_handle_complaint_not_found(self):
        data = {
            'complaint_id': 999,
            'is_remove': 'true',
            'reason': 'Violation of terms'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '投诉记录不存在')

    def test_handle_complaint_exception(self):
        with patch('complaint.models.Complaint.objects.get') as mock_get:
            mock_get.side_effect = Exception('Unexpected error')
            data = {
                'complaint_id': self.complaint_song.id,
                'is_remove': 'true',
                'reason': 'Violation of terms'
            }
            response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json()['success'], False)
            self.assertEqual(response.json()['message'], 'Unexpected error')

    def tearDown(self):
        self.song.delete()
        self.songlist.delete()
        self.complaint_song.delete()
        self.complaint_songlist.delete()
        self.admin_user.delete()
        self.normal_user.delete()
        self.complainer.delete()
        self.complained.delete()


class GetComplaintTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_complaint')
        self.admin_user = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.normal_user = User.objects.create(
            username='normaluser',
            email='normaluser@example.com',
            password='password',
            role='user'
        )
        self.complainer = User.objects.create(
            username='complainer',
            email='complainer@example.com',
            password='password'
        )
        self.complained = User.objects.create(
            username='complained',
            email='complained@example.com',
            password='password'
        )
        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.complained,
            visible=True
        )
        self.complaint = Complaint.objects.create(
            complainer=self.complainer,
            complained=self.complained,
            content='Test complaint content',
            object_type='song',
            object_id=self.song.id
        )
        self.token = generate_token('adminuser', 'admin')

    def test_get_complaint_success(self):
        response = self.client.get(self.url, {'complaint_id': self.complaint.id}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取投诉信息成功')
        self.assertIn('data', response.json())
        self.assertEqual(response.json()['data']['id'], self.complaint.id)

    def test_get_complaint_no_permission(self):
        self.token = generate_token('normaluser', 'user')
        response = self.client.get(self.url, {'complaint_id': self.complaint.id}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '没有权限访问')

    def test_get_complaint_missing_id(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '未传入complaint_id')

    def test_get_complaint_not_found(self):
        response = self.client.get(self.url, {'complaint_id': 999}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '投诉记录不存在')

    def tearDown(self):
        self.song.delete()
        self.complaint.delete()
        self.admin_user.delete()
        self.normal_user.delete()
        self.complainer.delete()
        self.complained.delete()


class AppealTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('appeal')
        self.admin_user = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.normal_user = User.objects.create(
            username='normaluser',
            email='normaluser@example.com',
            password='password',
            role='user'
        )
        self.complainer = User.objects.create(
            username='complainer',
            email='complainer@example.com',
            password='password'
        )
        self.complained = User.objects.create(
            username='complained',
            email='complained@example.com',
            password='password'
        )
        self.complaint = Complaint.objects.create(
            complainer=self.complainer,
            complained=self.complained,
            content='Test complaint content',
            object_type='song',
            object_id=1
        )
        self.token_complained = generate_token('complained', 'user')
        self.token_other = generate_token('normaluser', 'user')

    def test_appeal_success(self):
        data = {
            'complaint_id': self.complaint.id,
            'reason': 'This is an appeal reason'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token_complained)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], ' 申诉发送成功')

    def test_appeal_no_permission(self):
        data = {
            'complaint_id': self.complaint.id,
            'reason': 'This is an appeal reason'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token_other)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '没有权限访问')

    def test_appeal_complaint_not_found(self):
        data = {
            'complaint_id': 999,
            'reason': 'This is an appeal reason'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token_complained)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '投诉记录不存在')

    def tearDown(self):
        self.complaint.delete()
        self.admin_user.delete()
        self.normal_user.delete()
        self.complainer.delete()
        self.complained.delete()


class GetAppealTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_appeal')
        self.admin_user = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.normal_user = User.objects.create(
            username='normaluser',
            email='normaluser@example.com',
            password='password',
            role='user'
        )
        self.complainer = User.objects.create(
            username='complainer',
            email='complainer@example.com',
            password='password'
        )
        self.complained = User.objects.create(
            username='complained',
            email='complained@example.com',
            password='password'
        )
        self.complaint = Complaint.objects.create(
            complainer=self.complainer,
            complained=self.complained,
            content='Test complaint content',
            object_type='song',
            object_id=1
        )
        self.message = Message.objects.create(
            sender=self.complained,
            receiver=self.admin_user,
            title='申诉',
            content=f"{self.complaint.id} Appeal reason",
            type=7,
            is_read=False
        )
        self.token_admin = generate_token('adminuser', 'admin')
        self.token_user = generate_token('normaluser', 'user')

    def test_get_appeal_success(self):
        response = self.client.get(self.url, {'message_id': self.message.id}, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取申诉信息成功')
        self.assertIn('data', response.json())
        self.assertEqual(response.json()['data']['complaint']['id'], self.complaint.id)
        self.assertEqual(response.json()['data']['reason'], 'Appeal reason')

    def test_get_appeal_no_permission(self):
        response = self.client.get(self.url, {'message_id': self.message.id}, HTTP_AUTHORIZATION=self.token_user)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '没有权限访问')

    def test_get_appeal_missing_message_id(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '未传入message_id')

    def test_get_appeal_message_not_found(self):
        response = self.client.get(self.url, {'message_id': 999}, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '申诉消息记录不存在')

    def tearDown(self):
        self.complaint.delete()
        self.message.delete()
        self.admin_user.delete()
        self.normal_user.delete()
        self.complainer.delete()
        self.complained.delete()


class HandleAppealTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('handle_appeal')
        self.admin_user = User.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            password='password',
            role='admin'
        )
        self.normal_user = User.objects.create(
            username='normaluser',
            email='normaluser@example.com',
            password='password',
            role='user'
        )
        self.complainer = User.objects.create(
            username='complainer',
            email='complainer@example.com',
            password='password'
        )
        self.complained = User.objects.create(
            username='complained',
            email='complained@example.com',
            password='password'
        )
        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.complained,
            visible=False
        )
        self.songlist = SongList.objects.create(
            title='Test SongList',
            owner=self.complained,
            visible=False
        )
        self.complaint_song = Complaint.objects.create(
            complainer=self.complainer,
            complained=self.complained,
            content='Test complaint content',
            object_type='song',
            object_id=self.song.id
        )
        self.complaint_songlist = Complaint.objects.create(
            complainer=self.complainer,
            complained=self.complained,
            content='Test complaint content',
            object_type='songlist',
            object_id=self.songlist.id
        )
        self.token_admin = generate_token('adminuser', 'admin')
        self.token_user = generate_token('normaluser', 'user')

    def test_handle_appeal_success_recover_song(self):
        data = {
            'complaint_id': self.complaint_song.id,
            'is_recover': 'true',
            'reason': 'The issue has been resolved'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '处理申诉成功')
        self.song.refresh_from_db()
        self.assertTrue(self.song.visible)

    def test_handle_appeal_success_keep_song_down(self):
        data = {
            'complaint_id': self.complaint_song.id,
            'is_recover': 'false',
            'reason': 'The content is still inappropriate'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '处理申诉成功')
        self.song.refresh_from_db()
        self.assertFalse(self.song.visible)

    def test_handle_appeal_success_recover_songlist(self):
        data = {
            'complaint_id': self.complaint_songlist.id,
            'is_recover': 'true',
            'reason': 'The issue has been resolved'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '处理申诉成功')
        self.songlist.refresh_from_db()
        self.assertTrue(self.songlist.visible)

    def test_handle_appeal_no_permission(self):
        data = {
            'complaint_id': self.complaint_song.id,
            'is_recover': 'true',
            'reason': 'The issue has been resolved'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token_user)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '没有权限访问')

    def test_handle_appeal_complaint_not_found(self):
        data = {
            'complaint_id': 999,
            'is_recover': 'true',
            'reason': 'The issue has been resolved'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '投诉消息记录不存在')

    def test_handle_appeal_exception(self):
        with patch('complaint.models.Complaint.objects.get') as mock_get:
            mock_get.side_effect = Exception('Unexpected error')
            data = {
                'complaint_id': self.complaint_song.id,
                'is_recover': 'true',
                'reason': 'The issue has been resolved'
            }
            response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token_admin)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json()['success'], False)
            self.assertEqual(response.json()['message'], 'Unexpected error')

    def tearDown(self):
        self.song.delete()
        self.songlist.delete()
        self.complaint_song.delete()
        self.complaint_songlist.delete()
        self.admin_user.delete()
        self.normal_user.delete()
        self.complainer.delete()
        self.complained.delete()