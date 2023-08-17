from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from api.v1.serializers import IngredientSerializer
from users.models import User
from recipy.models import Ingredient

class IngredientTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@email.com",
            username='testname',
            first_name='test_first_name',
            last_name='test_last_name'
        )
        self.user.set_password("password")
        self.user.save()
        self.ingredient1=Ingredient.objects.create(
            name='ingredient_name1',
            measurement_unit = "measurement_unit1"
        )
        self.ingredient1=Ingredient.objects.create(
            name='ingredient_name2',
            measurement_unit = "measurement_unit2"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_tag(self):
        """Тест получение всех ингредиентов"""
        url = "/api/ingredients/"
        response = self.client.get(url, format='json')
        ingredient1_data = {'id': 1, 'name': 'ingredient_name1', 'measurement_unit': 'measurement_unit1'}
        ingredient2_data = {'id': 2, 'name': 'ingredient_name2', 'measurement_unit': 'measurement_unit2'}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(IngredientSerializer(response.data[0]).data==ingredient1_data)
        self.assertTrue(IngredientSerializer(response.data[1]).data==ingredient2_data)

