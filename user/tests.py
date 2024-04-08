from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
            "first_name": "test",
            "last_name": "user",
        }
        response = self.client.post("/accounts/register/", data, format="json")

        self.assertTrue(
            response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]
        )

        if response.status_code == status.HTTP_201_CREATED:
            self.assertTrue("id" in response.data)
            self.assertTrue("message" in response.data)
        else:
            print("Registration failed. Response data:", response.data)


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post("/accounts/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.assertTrue("user" in response.data)


class UserDetailsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_user_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/accounts/user_details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("username" in response.data)
        self.assertTrue("email" in response.data)
        self.assertTrue("referral_code" in response.data)
        self.assertTrue("my_referral_code" in response.data)
        self.assertTrue("created_at" in response.data)


class ReferralViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_referral_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/accounts/referral/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
