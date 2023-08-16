from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from users.models import User

class UserTests(APITestCase):


    def test_create_account(self):
        """Тестирование создание пользователя"""
        self.assertEqual(User.objects.count(), 0)
        url = "/api/users/"
        data = {
                    "email": "mail@mail.ru",
                    "username": "username",
                    "password": "456852Zx",
                    "first_name": "Nikita",
                    "last_name": "Romanov"
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'username')

    def test_get_token(self):
        """Получение Токена"""
        url = "/api/auth/token/login/"
        data = {
            "email": "nikox121@mail.ru",
            "password": "456852Zxы"
        }

    def test_set_password(self):
        url = "/api/users/set_password/"
        data = {
            "new_password": "456852Zxы",
            "current_password": "456852Zx"
        }

    def test_me_page(self):
        """Получение данных о себе"""
        user = User.objects.get(username='olivia')
        url = "/api/users/me/"
        response = self.client.get(url, format='json')
    
    def test_get_user(self):
        """Получение данных о всех пользователях"""
        url = "/api/users/2/"
