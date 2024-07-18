from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserTests(APITestCase):

    def test_register_user(self):
        url = reverse('register')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')


class UserViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            name='Test User'
        )
        self.client.force_authenticate(user=self.user)  # Authenticate the user

    def test_get_user(self):
        url = reverse('user')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['name'], self.user.name)


class LoginViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            name='Test User'
        )

    def test_login_success(self):
        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        print(response.data["message"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('access', response.data['token'])
        self.assertIn('refresh', response.data['token'])

    def test_login_failure_wrong_password(self):
        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Incorrect password')

    def test_login_failure_user_not_found(self):
        url = reverse('login')
        data = {
            'email': 'nonexistentuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'user not found')

