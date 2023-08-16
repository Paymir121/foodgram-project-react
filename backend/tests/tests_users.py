from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from users.models import User

class UserTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(
            email="test@email.com",
            username='testname',
            first_name='test_first_name',
            last_name='test_last_name'
        )
        self.user.set_password("password")
        self.user.save()

        self.user2 = User.objects.create(
            email="test2@email.com",
            username='testname2',
            first_name='test_first_name2',
            last_name='test_last_name2'
        )
        self.user2.set_password("password2")
        self.user2.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    # def test_create_account(self):
    #     """Тестирование создание пользователя"""
    #     self.assertEqual(User.objects.count(), 2)
    #     url = "/api/users/"
    #     data = {
    #                 "email": "mail@mail.ru",
    #                 "username": "username",
    #                 "password": "456852Zx",
    #                 "first_name": "Nikita",
    #                 "last_name": "Romanov"
    #             }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(User.objects.count(), 3)
    #     self.assertEqual(User.objects.get(id=3).username, 'username')

    def test_get_token(self):
        """Получение Токена"""
        url = "/api/auth/token/login/"
        data = {
            "email": "test@email.com",
            "password": "password"
        }
        # token = Token.objects.get(user__username='testname')
        # response = self.client.post(url, data, format='json')
        # self.assertEqual(response.data['auth_token'])

    def test_set_wrong_password(self):
        """Смена пароля с неправильным паролем"""
        url = "/api/users/set_password/"
        data = {
            "new_password": "456852Zxы",
            "current_password": "456852Zx"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_right_password(self):  
        """Смена пароля с неправильным паролем"""
        url = "/api/users/set_password/"
        data = {
            "new_password": "456852Zxы",
            "current_password": "password"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # self.assertEqual(self.user.password, data['new_password']) # Решить проблему с шифровкой пароля

    def test_me_page(self):
        """Получение данных о себе"""
        url = "/api/users/me/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.data['username'], self.user.username)

    
    def test_get_user(self):
        """Получение данных о всех пользователях"""
        url = "/api/users/"
        response = self.client.get(url, format='json')
        users = response.data['results']
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(users[1]['email'], self.user.email)
        self.assertEqual(users[0]['email'], self.user2.email)

    def test_get_user(self):
        """Получение данных о пользователе"""
        url = "/api/users/1/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.data['email'], self.user.email)

