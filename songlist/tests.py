from django.test import TestCase, Client
from django.urls import reverse
from .models import User, SongList
from user.tests import generate_token


class GetUserSonglistsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_user_songlists')
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.songlist1 = SongList.objects.create(
            title='Songlist 1',
            owner=self.user,
            visible=True
        )
        self.songlist2 = SongList.objects.create(
            title='Songlist 2',
            owner=self.user,
            visible=False
        )
        self.token = generate_token('testuser', 'user')

    def test_get_user_songlists_missing_username(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False, 'message': '缺少用户姓名'})

    def test_get_user_songlists_user_not_exist(self):
        response = self.client.get(self.url, {'username': 'nonexistentuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'success': False, 'message': '用户不存在'})

    def test_get_user_songlists_success(self):
        response = self.client.get(self.url, {'username': 'testuser'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], '获取用户歌单成功')
        self.assertEqual(len(response.json()['data']), 1)
        self.assertEqual(response.json()['data'][0]['title'], 'Songlist 1')

    def test_get_user_songlists_missing_token(self):
        response = self.client.get(self.url, {'username': 'testuser'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Authorization header missing'})

    def test_get_user_songlists_invalid_token(self):
        response = self.client.get(self.url, {'username': 'testuser'}, HTTP_AUTHORIZATION='Bearer invalid_token')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'success': False, 'message': 'Invalid token'})

    def tearDown(self):
        self.user.delete()
        self.songlist1.delete()
        self.songlist2.delete()

