from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from users.models import User
from recipy.models import Tag

class TagTests(APITestCase):

    def test_get_tag(self):
        """Тест получение всех тагов"""
        url = "/api/tags/"
