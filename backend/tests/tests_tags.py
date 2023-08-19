from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.v1.serializers import TagSerializer
from recipy.models import Tag
from users.models import User


class TagTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@email.com",
            username="testname",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.user.set_password("password")
        self.user.save()
        self.tag1 = Tag.objects.create(
            name="tag_name1", color="color_tag1", slug="slug1"
        )
        self.tag2 = Tag.objects.create(
            name="tag_name2", color="color_tag2", slug="slug2"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_tag(self):
        """Тест получение всех тагов"""
        url = "/api/tags/"
        response = self.client.get(url, format="json")
        tag1_data = {
            "id": 1,
            "name": "tag_name1",
            "color": "color_tag1",
            "slug": "slug1",
        }
        tag2_data = {
            "id": 2,
            "name": "tag_name2",
            "color": "color_tag2",
            "slug": "slug2",
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TagSerializer(response.data[0]).data == tag1_data)
        self.assertTrue(TagSerializer(response.data[1]).data == tag2_data)
