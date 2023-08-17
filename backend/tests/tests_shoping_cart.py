# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from rest_framework.test import force_authenticate

# from users.models import User, Follow
# from recipy.models import (Tag,
#                            Ingredient,
#                            Recipy,
#                            Favorite,
#                            ShoppingCart)


# class ShopingCartTests(APITestCase):

#     def test_post_shoping_cart(self):
#         """Добавление рецепта в корзину"""
#         url = "/api/recipes/1/shopping_cart/"
#         response = self.client.get(url, format='json')

#     def test_delete_shoping_cart(self):
#         """Удаление рецепта в корзину"""
#         url = "/api/recipes/1/shopping_cart/"
#         response = self.client.get(url, format='json')

#     def test_get_shoping_cart(self):
#         """Получить файл с ингредиентами для рецептов в корзине"""
#         url = "/api/recipes/download_shopping_cart/"
#         response = self.client.get(url, format='json')
