from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from message.models import Message
from user.tests import generate_token
from .models import Song, Comment, User


class AddCommentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('add_comment')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.uploader = User.objects.create(
            username='uploader',
            email='uploader@example.com',
            password='password'
        )
        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.uploader,
            visible=True
        )
        self.token = generate_token('testuser', 'user')

    def test_add_comment_success(self):
        data = {
            'songID': self.song.id,
            'content': 'This is a test comment.'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '评论成功')
        self.assertTrue(Comment.objects.filter(user=self.user, song=self.song, content='This is a test comment.').exists())

    def test_add_comment_song_not_exist(self):
        data = {
            'songID': 999,
            'content': 'This is a test comment.'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertIn('Song matching query does not exist', response.json()['message'])

    def test_add_comment_user_not_exist(self):
        self.user.delete()
        data = {
            'songID': self.song.id,
            'content': 'This is a test comment.'
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertIn('User matching query does not exist', response.json()['message'])

    def test_add_comment_missing_content(self):
        data = {
            'songID': self.song.id
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertIn('content', response.json()['message'])

class DeleteCommentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('delete_comment')
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
        self.uploader = User.objects.create(
            username='uploader',
            email='uploader@example.com',
            password='password'
        )
        self.song = Song.objects.create(
            title='Test Song',
            singer='Test Singer',
            uploader=self.uploader,
            visible=True
        )
        self.comment = Comment.objects.create(
            user=self.normal_user,
            song=self.song,
            content='This is a test comment.'
        )
        self.message = Message.objects.create(
            sender=self.normal_user,
            receiver=self.uploader,
            title='新的评论',
            content=f"{self.normal_user.username}评论了你上传的歌曲《{self.song.title}》：{self.comment.content}",
            type=2
        )
        self.token_admin = generate_token('adminuser', 'admin')
        self.token_user = generate_token('normaluser', 'user')
        self.token_other_user = generate_token('otheruser', 'user')

    def test_delete_comment_success_admin(self):
        response = self.client.get(self.url, {'commentID': self.comment.id}, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '评论删除成功')
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())

    def test_delete_comment_success_user(self):
        response = self.client.get(self.url, {'commentID': self.comment.id}, HTTP_AUTHORIZATION=self.token_user)
        self.assertEqual(response.json()['message'], '评论删除成功')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())

    def test_delete_comment_no_permission(self):
        response = self.client.get(self.url, {'commentID': self.comment.id}, HTTP_AUTHORIZATION=self.token_other_user)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], '没有权限删除')
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())
        self.assertTrue(Message.objects.filter(id=self.message.id).exists())

    def test_delete_comment_not_exist(self):
        response = self.client.get(self.url, {'commentID': 999}, HTTP_AUTHORIZATION=self.token_admin)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertIn('Comment matching query does not exist', response.json()['message'])

    def tearDown(self):
        self.song.delete()
        self.normal_user.delete()
        self.uploader.delete()
        self.admin_user.delete()
        Comment.objects.all().delete()
