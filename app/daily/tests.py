from django.test import Client, TestCase
from django.urls import reverse

from .models import Users, PostFoods


class LoginTests(TestCase):
    """user_loginのテストクラス"""

    def test_get(self):
        """Getメソッドでのリクエスト時にステータスコード200で返却されるか"""
        response = self.client.get(reverse('daily:user_login'))
        self.assertEqual(response.status_code, 200)


class UserTests(TestCase):
    """usersテーブルのテストクラス"""

    def setUp(self):
        """
        メソッド名「setUp」とすることで、テスト用データ作成。
        同クラス内で共通で使用するユーザーを作成。
        """
        user = Users.objects.create(username='test11', age='1', email='test11@gmail.com', is_active=True, password='test1234')

    def test_login_user(self):
        """作成ユーザーへログイン可能か確認。200で返却されること"""
        response = self.client.post(path='', data={'email': 'test@gmail.com', 'password': 'test1234'})
        self.assertEqual(response.status_code, 200)
