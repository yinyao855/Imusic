from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock

from follow.models import Follow
from message.views import send_message
from user.models import User
from message.models import Message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from user.tests import generate_token


class SendMessageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_sender = User.objects.create(
            username='testsender',
            email='testsender@example.com',
            password='password'
        )
        self.user_receiver = User.objects.create(
            username='testreceiver',
            email='testreceiver@example.com',
            password='password'
        )
        self.url = reverse('send')
        self.token = generate_token(self.user_sender.username, self.user_sender.role)

    @patch('message.views.send_message')
    def test_send_message_success(self, mock_send_message):
        data = {
            'receiver': self.user_receiver.username,
            'content': 'Hello, this is a test message.'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '消息发送成功')
        mock_send_message.assert_called_once_with(
            '私信', 'Hello, this is a test message.', 5, self.user_sender, self.user_receiver
        )

    def test_send_message_empty_content(self):
        data = {
            'receiver': self.user_receiver.username,
            'content': ''
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '消息内容不能为空')

    def test_send_message_user_does_not_exist(self):
        data = {
            'receiver': 'nonexistentuser',
            'content': 'Hello, this is a test message.'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '用户不存在')

    @patch('message.views.send_message')
    def test_send_message_internal_error(self, mock_send_message):
        mock_send_message.side_effect = Exception('Internal server error')
        data = {
            'receiver': self.user_receiver.username,
            'content': 'Hello, this is a test message.'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Internal server error')

    def tearDown(self):
        self.user_sender.delete()
        self.user_receiver.delete()


class GetReceivedMessagesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testreceiver',
            email='testreceiver@example.com',
            password='password'
        )
        self.sender = User.objects.create(
            username='testsender',
            email='testsender@example.com',
            password='password'
        )
        self.message1 = Message.objects.create(
            sender=self.sender,
            receiver=self.user,
            title='Message 1',
            content='This is a test message.',
            type=1
        )
        self.message2 = Message.objects.create(
            sender=self.sender,
            receiver=self.user,
            title='Message 2',
            content='This is another test message.',
            type=2
        )
        self.private_message = Message.objects.create(
            sender=self.sender,
            receiver=self.user,
            title='Private Message',
            content='This is a private message.',
            type=5
        )
        self.url = reverse('received')
        self.token = generate_token(self.user.username, self.user.role)

    def test_get_received_messages_success(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取用户消息成功')
        self.assertIn('data', response.json())
        messages_data = response.json()['data']
        self.assertEqual(len(messages_data), 2)

    def test_get_received_messages_user_does_not_exist(self):
        invalid_token = generate_token('nonexistentuser', 'user')
        response = self.client.get(self.url, HTTP_AUTHORIZATION=invalid_token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '用户不存在')

    @patch('message.views.Message.objects.filter')
    def test_get_received_messages_internal_error(self, mock_message_filter):
        mock_message_filter.side_effect = Exception('Internal server error')
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Internal server error')

    def tearDown(self):
        self.user.delete()
        self.sender.delete()
        self.message1.delete()
        self.message2.delete()
        self.private_message.delete()


class GetSentMessagesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_sender = User.objects.create(
            username='testsender',
            email='testsender@example.com',
            password='password'
        )
        self.user_receiver = User.objects.create(
            username='testreceiver',
            email='testreceiver@example.com',
            password='password'
        )
        self.message1 = Message.objects.create(
            sender=self.user_sender,
            receiver=self.user_receiver,
            title='Private Message 1',
            content='This is a private message 1.',
            type=5
        )
        self.message2 = Message.objects.create(
            sender=self.user_sender,
            receiver=self.user_receiver,
            title='Private Message 2',
            content='This is a private message 2.',
            type=5
        )
        self.non_private_message = Message.objects.create(
            sender=self.user_sender,
            receiver=self.user_receiver,
            title='Public Message',
            content='This is a public message.',
            type=1
        )
        self.url = reverse('get_sent')
        self.token = generate_token(self.user_sender.username, self.user_sender.role)

    def test_get_sent_messages_success(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取用户消息成功')
        self.assertIn('data', response.json())
        messages_data = response.json()['data']
        self.assertEqual(len(messages_data), 2)

    def test_get_sent_messages_user_does_not_exist(self):
        invalid_token = generate_token('nonexistentuser', 'user')
        response = self.client.get(self.url, HTTP_AUTHORIZATION=invalid_token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '用户不存在')

    @patch('message.views.Message.objects.filter')
    def test_get_sent_messages_internal_error(self, mock_message_filter):
        mock_message_filter.side_effect = Exception('Internal server error')
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Internal server error')

    def tearDown(self):
        self.user_sender.delete()
        self.user_receiver.delete()
        self.message1.delete()
        self.message2.delete()
        self.non_private_message.delete()


class ReadMessageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_receiver = User.objects.create(
            username='testreceiver',
            email='testreceiver@example.com',
            password='password'
        )
        self.user_sender = User.objects.create(
            username='testsender',
            email='testsender@example.com',
            password='password'
        )
        self.message = Message.objects.create(
            sender=self.user_sender,
            receiver=self.user_receiver,
            title='Test Message',
            content='This is a test message.',
            type=5,
            is_read=False
        )
        self.url = reverse('read')
        self.token = generate_token(self.user_receiver.username, self.user_receiver.role)

    def test_read_message_success(self):
        data = {'message_id': self.message.id}
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '消息已读')
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)

    def test_read_message_not_owned_by_user(self):
        other_user_token = generate_token('otheruser', 'user')
        data = {'message_id': self.message.id}
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=other_user_token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '这不是您的消息')
        self.message.refresh_from_db()
        self.assertFalse(self.message.is_read)

    def test_read_message_does_not_exist(self):
        data = {'message_id': 99999}
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '消息不存在')

    def tearDown(self):
        self.user_receiver.delete()
        self.user_sender.delete()
        self.message.delete()

""" 
测试delete_message的时候需要注释掉@require_http_methods(["DELETE"])
原因是delete_message规定的是DELETE方法，但是函数里面却使用了GET方法的request.GET
导致测试代码只能以GET的形式发送请求
"""
class DeleteMessageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_sender = User.objects.create(
            username='testsender',
            email='testsender@example.com',
            password='password'
        )
        self.user_receiver = User.objects.create(
            username='testreceiver',
            email='testreceiver@example.com',
            password='password'
        )
        self.message = Message.objects.create(
            sender=self.user_sender,
            receiver=self.user_receiver,
            title='Test Message',
            content='This is a test message.',
            type=1,
            is_read=False
        )
        self.url = reverse('delete')
        self.token = generate_token(self.user_receiver.username, self.user_receiver.role)

    def test_delete_message_success(self):
        response = self.client.get(self.url, {'message_id': self.message.id}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '消息已删除')
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())

    def test_delete_message_not_found(self):
        response = self.client.get(self.url, {'message_id': 99999}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '消息不存在')

    def test_delete_message_no_permission(self):
        self.message.type = 5
        self.message.save()
        response = self.client.get(self.url, {'message_id': self.message.id}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.json()['message'], '无删除权限')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['success'], False)

    def test_delete_message_sender_no_permission(self):
        self.token = generate_token(self.user_sender.username, self.user_sender.role)
        response = self.client.get(self.url, {'message_id': self.message.id}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '无删除权限')

    def tearDown(self):
        self.user_sender.delete()
        self.user_receiver.delete()
        self.message.delete()


class SearchPrivateMessagesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_sender = User.objects.create(
            username='testsender',
            email='testsender@example.com',
            password='password'
        )
        self.user_receiver = User.objects.create(
            username='testreceiver',
            email='testreceiver@example.com',
            password='password'
        )
        self.message1 = Message.objects.create(
            sender=self.user_sender,
            receiver=self.user_receiver,
            title='Message 1',
            content='This is a test message.',
            type=5
        )
        self.message2 = Message.objects.create(
            sender=self.user_receiver,
            receiver=self.user_sender,
            title='Message 2',
            content='This is another test message.',
            type=5
        )
        self.url = reverse('private')
        self.token = generate_token(self.user_sender.username, self.user_sender.role)

    @patch('message.views.handle_private_messages')
    def test_search_private_messages_success(self, mock_handle_private_messages):
        mock_handle_private_messages.return_value = (True, [
            self.message1.to_dict(),
            self.message2.to_dict()
        ])
        response = self.client.get(self.url, {'friend': self.user_receiver.username}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取私信消息成功')
        self.assertIn('data', response.json())
        messages_data = response.json()['data']
        self.assertEqual(len(messages_data), 2)

    def test_search_private_messages_user_does_not_exist(self):
        response = self.client.get(self.url, {'friend': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '用户不存在')

    @patch('message.views.handle_private_messages')
    def test_search_private_messages_internal_error(self, mock_handle_private_messages):
        mock_handle_private_messages.side_effect = Exception('Internal server error')
        response = self.client.get(self.url, {'friend': self.user_receiver.username}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Internal server error')

    def tearDown(self):
        self.user_sender.delete()
        self.user_receiver.delete()
        self.message1.delete()
        self.message2.delete()


class SearchChatsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.friend1 = User.objects.create(
            username='friend1',
            email='friend1@example.com',
            password='password'
        )
        self.friend2 = User.objects.create(
            username='friend2',
            email='friend2@example.com',
            password='password'
        )
        Follow.objects.create(follower=self.user, followed=self.friend1)
        Follow.objects.create(follower=self.friend2, followed=self.user)

        self.url = reverse('search')
        self.token = generate_token(self.user.username, self.user.role)

    @patch('message.views.handle_private_messages')
    def test_search_chats_success(self, mock_handle_private_messages):
        mock_handle_private_messages.side_effect = [
            ('Last message with friend1', []),
            ('Last message with friend2', [])
        ]
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取聊天信息成功')
        self.assertIn('data', response.json())
        chat_data = response.json()['data']
        self.assertEqual(len(chat_data), 2)
        self.assertEqual(chat_data[0]['friend'], 'friend1')
        self.assertEqual(chat_data[1]['friend'], 'friend2')

    def test_search_chats_user_does_not_exist(self):
        invalid_token = generate_token('nonexistentuser', 'user')
        response = self.client.get(self.url, HTTP_AUTHORIZATION=invalid_token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '用户不存在')

    @patch('message.views.handle_private_messages')
    def test_search_chats_internal_error(self, mock_handle_private_messages):
        mock_handle_private_messages.side_effect = Exception('Internal server error')
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Internal server error')

    def tearDown(self):
        self.user.delete()
        self.friend1.delete()
        self.friend2.delete()