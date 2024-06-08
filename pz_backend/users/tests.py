from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from django.urls import reverse

from .serializers import UserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    def test_valid_data(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "password_confirm": "testpassword",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))

    def test_passwords_do_not_match(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "password_confirm": "differentpassword",
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]), "Passwords do not match."
        )

    def test_missing_password_confirm(self):
        data = {"username": "testuser", "password": "testpassword"}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password_confirm", serializer.errors)


class UserCreateViewTest(APITestCase):
    def test_create_user(self):
        url = reverse("user-register")
        data = {
            "username": "testuser",
            "password": "testpassword",
            "password_confirm": "testpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_passwords_do_not_match(self):
        url = reverse("user-register")
        data = {
            "username": "testuser",
            "password": "testpassword",
            "password_confirm": "differentpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0], "Passwords do not match."
        )

    def test_missing_password_confirm(self):
        url = reverse("user-register")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password_confirm", response.data)


class CustomAuthTokenTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.login_url = reverse("user-login")

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user_id"], self.user.id)
        self.assertEqual(response.data["username"], "testuser")

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)

    def test_login_with_nonexistent_user(self):
        response = self.client.post(
            self.login_url, {"username": "nonexistent", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)
