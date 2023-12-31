from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.v1.serializers import IngredientSerializer
from recipy.models import Ingredient
from users.models import User


class IngredientTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@email.com",
            username="testname",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.user.set_password("password")
        self.user.save()
        self.ingredient1 = Ingredient.objects.create(
            name="ingredient_name1", measurement_unit="measurement_unit1"
        )
        self.ingredient1 = Ingredient.objects.create(
            name="ingredient_name2", measurement_unit="measurement_unit2"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_tag(self):
        """Тест получение всех ингредиентов"""
        url = "/api/ingredients/"
        response = self.client.get(url, format="json")
        ingredient1_data = {
            "id": 1,
            "name": "ingredient_name1",
            "measurement_unit": "measurement_unit1",
        }
        ingredient2_data = {
            "id": 2,
            "name": "ingredient_name2",
            "measurement_unit": "measurement_unit2",
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient1 = IngredientSerializer(response.data[0]).data
        ingredient2 = IngredientSerializer(response.data[1]).data
        self.assertTrue(ingredient1 == ingredient1_data)
        self.assertTrue(ingredient2 == ingredient2_data)
