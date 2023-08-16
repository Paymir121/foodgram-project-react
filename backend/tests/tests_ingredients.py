from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from users.models import User
from recipy.models import Ingredient

class IngredienTests(APITestCase):


    def test_get_ingredient(self):
        """Получение всех ингредиентов"""
        url = "/api/ingredients/"
