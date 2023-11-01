from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from users.models import getKey, User


class UserSerializerTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "username": "johndoe",
            "password": "securepassword"
        }

    def test_user_register_serializer(self):
        response = self.client.post(reverse("register"), self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_check_activation_code_serializer(self):
        # First, create a user and generate an activation code
        user_data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "username": "johndoe",
            "password": "securepassword"
        }
        response = self.client.post(reverse("register"), user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        activation_data = {
            "email": "john@example.com",
            "activate_code": getKey("john@example.com")["activate_code"]
        }
        response = self.client.post(reverse("check_activation_code"), activation_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_serializer(self):
        response = self.client.post(reverse("reset_password"), {"email": "john@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_confirm_serializer(self):
        activation_data = {
            "email": "john@example.com",
            "activation_code": getKey("john@example.com")["activate_code"],
            "new_password": "newpassword",
            "confirm_password": "newpassword"
        }
        response = self.client.post(reverse("reset_password_confirm"), activation_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
