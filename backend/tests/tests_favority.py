from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from users.models import User, Follow
from recipy.models import (Tag,
                           Ingredient,
                           Recipy,
                           Favorite,
                           ShoppingCart)

class FavoriteTests(APITestCase):


    def test_post_favorite(self):
        """Добавление в избранное"""
        url = "/api/recipes/1/favorite/"

    def test_delete_favorite(self):
        """Удаление из избранного"""
        url = "/api/recipes/1/favorite/"
