import datetime
import jwt
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from .models import User, Follow
from message.models import Message
from user.tests import generate_token


class FollowUnfollowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('follow_unfollow')
        self.user1 = User.objects.create(
            username='user1',
            email='user1@example.com',
            password='password'
        )
        self.user2 = User.objects.create(
            username='user2',
            email='user2@example.com',
            password='password'
        )
        self.token_user1 = generate_token('user1', 'user')

    def test_follow_unfollow_missing_username(self):
        response = self.client.post(self.url, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少对象用户的姓名'})

    def test_follow_user_success(self):
        response = self.client.post(self.url, {'username': 'user2'}, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True, 'message': '加关注成功'})
        self.assertTrue(Follow.objects.filter(follower=self.user1, followed=self.user2).exists())
        self.assertEqual(Message.objects.filter(sender=self.user1, receiver=self.user2).count(), 1)
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.assertEqual(self.user1.following_count, 1)
        self.assertEqual(self.user2.follower_count, 1)

    def test_unfollow_user_success(self):
        Follow.objects.create(follower=self.user1, followed=self.user2)
        Message.objects.create(sender=self.user1, receiver=self.user2, title='新的关注', content='user1关注了你',
                               type=5)

        response = self.client.post(self.url, {'username': 'user2'}, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True, 'message': '取消关注成功'})
        self.assertFalse(Follow.objects.filter(follower=self.user1, followed=self.user2).exists())
        self.assertEqual(Message.objects.filter(sender=self.user1, receiver=self.user2).count(), 0)
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.assertEqual(self.user1.following_count, 0)
        self.assertEqual(self.user2.follower_count, 0)

    def test_follow_unfollow_user_not_exist(self):
        response = self.client.post(self.url, {'username': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '对象用户不存在'})

    def test_follow_unfollow_internal_server_error(self):
        original_get = User.objects.get
        User.objects.get = lambda *args, **kwargs: 1 / 0  # exception

        response = self.client.post(self.url, {'username': 'user2'}, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['success'], False)

        User.objects.get = original_get

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()


class GetFollowingsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_followings')
        self.user1 = User.objects.create(
            username='user1',
            email='user1@example.com',
            password='password',
            permission_following=True
        )
        self.user2 = User.objects.create(
            username='user2',
            email='user2@example.com',
            password='password'
        )
        self.user3 = User.objects.create(
            username='user3',
            email='user3@example.com',
            password='password',
            permission_following=False
        )
        self.token_user1 = generate_token('user1', 'user')
        self.token_user2 = generate_token('user2', 'user')
        self.token_user3 = generate_token('user3', 'user')
        self.token_admin = generate_token('admin', 'admin')

        Follow.objects.create(follower=self.user1, followed=self.user2)
        Follow.objects.create(follower=self.user1, followed=self.user3)

    def test_get_followings_missing_username(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少对象用户的姓名'})

    def test_get_followings_success(self):
        response = self.client.get(self.url, {'username': 'user1'}, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取成功')
        self.assertEqual(len(response.json()['data']), 2)

    def test_get_followings_private_user_as_non_admin(self):
        response = self.client.get(self.url, {'username': 'user3'}, HTTP_AUTHORIZATION=self.token_user2)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'message': '获取失败，用户设置为隐私'})

    def test_get_followings_private_user_as_admin(self):
        response = self.client.get(self.url, {'username': 'user3'}, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取成功')

    def test_get_followings_user_not_exist(self):
        response = self.client.get(self.url, {'username': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '对象用户不存在'})

    def test_get_followings_self(self):
        response = self.client.get(self.url, {'username': 'user3'}, HTTP_AUTHORIZATION=self.token_user3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取成功')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()


class GetFollowersTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_followers')
        self.user1 = User.objects.create(
            username='user1',
            email='user1@example.com',
            password='password',
            permission_follower=True
        )
        self.user2 = User.objects.create(
            username='user2',
            email='user2@example.com',
            password='password'
        )
        self.user3 = User.objects.create(
            username='user3',
            email='user3@example.com',
            password='password',
            permission_follower=False
        )
        self.token_user1 = generate_token('user1', 'user')
        self.token_user2 = generate_token('user2', 'user')
        self.token_user3 = generate_token('user3', 'user')
        self.token_admin = generate_token('admin', 'admin')

        Follow.objects.create(follower=self.user1, followed=self.user2)
        Follow.objects.create(follower=self.user3, followed=self.user1)

    def test_get_followers_missing_username(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少对象用户的姓名'})

    def test_get_followers_success(self):
        response = self.client.get(self.url, {'username': 'user1'}, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取成功')
        self.assertEqual(len(response.json()['data']), 1)

    def test_get_followers_private_user_as_non_admin(self):
        response = self.client.get(self.url, {'username': 'user3'}, HTTP_AUTHORIZATION=self.token_user2)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'message': '获取失败，用户设置为隐私'})

    def test_get_followers_private_user_as_admin(self):
        response = self.client.get(self.url, {'username': 'user3'}, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取成功')

    def test_get_followers_user_not_exist(self):
        response = self.client.get(self.url, {'username': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '对象用户不存在'})

    def test_get_followers_self(self):
        response = self.client.get(self.url, {'username': 'user3'}, HTTP_AUTHORIZATION=self.token_user3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取成功')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()


class GetFriendsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_friends')
        self.user1 = User.objects.create(
            username='user1',
            email='user1@example.com',
            password='password'
        )
        self.user2 = User.objects.create(
            username='user2',
            email='user2@example.com',
            password='password'
        )
        self.user3 = User.objects.create(
            username='user3',
            email='user3@example.com',
            password='password',
            permission_follower=False
        )
        self.token_user1 = generate_token('user1', 'user')
        self.token_user2 = generate_token('user2', 'user')
        self.token_user3 = generate_token('user3', 'user')
        self.token_admin = generate_token('admin', 'admin')

        Follow.objects.create(follower=self.user1, followed=self.user2)
        Follow.objects.create(follower=self.user2, followed=self.user1)
        Follow.objects.create(follower=self.user1, followed=self.user3)
        Follow.objects.create(follower=self.user3, followed=self.user1)

    def test_get_friends_success(self):
        response = self.client.get(self.url, {'username': 'user1'}, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取成功')
        self.assertEqual(len(response.json()['data']), 2)

    def test_get_friends_private_user_as_non_admin(self):
        response = self.client.get(self.url, {'username': 'user3'}, HTTP_AUTHORIZATION=self.token_user2)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'success': False, 'message': '获取失败，用户设置为隐私'})

    def test_get_friends_private_user_as_admin(self):
        response = self.client.get(self.url, {'username': 'user3'}, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取成功')

    def test_get_friends_user_not_exist(self):
        response = self.client.get(self.url, {'username': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '对象用户不存在'})

    def test_get_friends_self(self):
        response = self.client.get(self.url, {'username': 'user3'}, HTTP_AUTHORIZATION=self.token_user3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取成功')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()