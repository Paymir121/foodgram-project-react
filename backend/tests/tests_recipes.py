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

class RecipyTests(APITestCase):


    def test_get_list_recipes(self):
        """Получение списка рецептов"""
        url = "/api/recipes/"

    def test_get_recipy(self):
        """Получение одного рецепта"""
        url = "/api/recipes/1/"

    def test_post_recipy(self):
        """Пост рецепта"""
        url = "/api/recipes/"
        data = {
                "ingredients": [
                    {
                    "id": 1123,
                    "amount": 10
                    }
                ],
                    "tags": [
                    1
                ],
                    "name": "recicpy2",
                    "image": null,
                    "text": "recipyvwqd",
                    "cooking_time": 34
                }

    def test_patch_recipy(self):
        """Редактирование рецепта"""
        url = "/api/recipes/"
        data = {
                "ingredients": [
                    {
                    "id": 2,
                    "amount": 13
                    }
                ],
                "tags": [
                    1
                ],
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
                "name": "recipy2",
                "text": "strdscsing",
                "cooking_time": 155
                }

    def test_get_list_recipes_filter_tag(self):
        """Получение списка рецептов отфильтрованный по Тагам"""
        url = "/api/recipes/?page=1&limit=6&tags=slug"
    
    def test_get_list_recipes_filter_author(self):
        """Получение списка рецептов отфильтрованный по авторам"""
        url = "/api/recipes/?page=1&limit=6&author=1"

    def test_get_list_recipes_filter_favorite(self):
        """Получение списка рецептов Избранные рецепты"""
        url = "/api/recipes/?page=1&limit=6&is_favorited=1"