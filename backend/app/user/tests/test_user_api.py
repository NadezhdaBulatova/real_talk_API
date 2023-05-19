"""
Tests for user-app endpoints
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.exceptions import ValidationError
from user.serializers import UserCreateSerializer
from rest_framework_simplejwt.tokens import AccessToken

def register_user(**kwargs):
    """Create and return new user"""
    return get_user_model().objects.create_user(**kwargs)

class PublicUserAPITests(TestCase):
    """Tests the unauthenticated endpoints of the user API"""
    def setUp(self):
        self.admin_credentials = {
            'email': 'admin@example.com',
            'password': '1234QWer!',
            'username': 'test_admin'
        }
        self.admin = register_user(**self.admin_credentials)
        self.client = APIClient()
        return super().setUp()
    
    def test_register_user_success(self):
        user_credentials = {
            'email': 'test@example.com',
            'password': '1234QWer!',
            'username': 'test_username'
        }
        register_url = reverse('user:register')
        res = self.client.post(register_url, user_credentials)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=user_credentials['email'])
        self.assertTrue(user.check_password(user_credentials['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        user_credentials = {
            'email': self.admin_credentials['email'],
            'password': '123456',
            'username': 'test_username'
        }
        register_url = reverse('user:register')
        res = self.client.post(register_url, user_credentials)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        user_credentials = {
            'email': 'test@example.com',
            'password': '12',
            'username': 'test_username'
        }
        register_url = reverse('user:register')
        res = self.client.post(register_url, user_credentials)
        self.assertRaises(ValidationError)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=user_credentials['email']).exists()
        self.assertFalse(user_exists)
    
    def test_incorrect_email_error(self):
        user_credentials = {
            'email': 'testexample.com',
            'password': '1234QWer!',
            'username': 'test_username'
        }
        register_url = reverse('user:register')
        res = self.client.post(register_url, user_credentials)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=user_credentials['email']).exists()
        self.assertFalse(user_exists)

    def test_user_detail_unauthenticated(self):
        user_detail_url = reverse('user:user-detail', kwargs={'id': self.admin.id})
        res = self.client.get(user_detail_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_detail_authenticated(self):
        user = register_user(email="user@example.com",
            password='1234QWer!',
            username='user')
        token = AccessToken.for_user(user)
        user_detail_url = reverse('user:user-detail', kwargs={'id': self.admin.id})
        headers = {'Authorization': f'Bearer {token}'}
        res = self.client.get(user_detail_url, headers = headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_obtain_pair(self):
        toke_obtain_pair_url = reverse('user:token_obtain_pair')
        data = {
            'email': self.admin_credentials['email'],
            'password': self.admin_credentials['password'],
        }
        res = self.client.post(toke_obtain_pair_url, data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, 'refresh')
        self.assertContains(res, 'access')

    def test_protected_route_with_access_token(self):
        toke_obtain_pair_url = reverse('user:token_obtain_pair')
        data = {
            'email': self.admin_credentials['email'],
            'password': self.admin_credentials['password'],
        }
        res = self.client.post(toke_obtain_pair_url, data=data)
        access_token = res.data['access']
        refresh_token = res.data['refresh']
        user_detail_url = reverse('user:user-detail', kwargs={'id': self.admin.id})
        success_headers = {'Authorization': f'Bearer {access_token}'}
        fail_headers = {'Authorization': f'Bearer {refresh_token}'}
        res_success = self.client.get(user_detail_url, headers = success_headers)
        self.assertEqual(res_success.status_code, status.HTTP_200_OK)
        res_fail = self.client.get(user_detail_url, headers = fail_headers)
        self.assertEqual(res_fail.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        toke_obtain_pair_url = reverse('user:token_obtain_pair')
        data = {
            'email': self.admin_credentials['email'],
            'password': self.admin_credentials['password'],
        }
        res_tokens = self.client.post(toke_obtain_pair_url, data=data)
        user_detail_url = reverse('user:user-detail', kwargs={'id': self.admin.id})
        res_protected_route = self.client.get(user_detail_url, 
                                              headers = {'Authorization': f'Bearer {res_tokens.data["access"]}'})
        self.assertEqual(res_protected_route.status_code, status.HTTP_200_OK)
        token_refresh_url = reverse('user:token_refresh')
        data = {'refresh': res_tokens.data['refresh']}
        response = self.client.post(token_refresh_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'access')
        self.assertNotEqual(response.data['access'], res_tokens.data["access"])
        res_protected_route = self.client.get(user_detail_url, headers = {'Authorization': f'Bearer {response.data["access"]}'})
        self.assertEqual(res_protected_route.status_code, status.HTTP_200_OK)

    def test_token_verify(self):
        toke_obtain_pair_url = reverse('user:token_obtain_pair')
        data = {
            'email': self.admin_credentials['email'],
            'password': self.admin_credentials['password'],
        }
        res_tokens = self.client.post(toke_obtain_pair_url, data=data)
        token_verify_url = reverse('user:token_verify')
        data = {
            'token': res_tokens.data['access']
        }
        response = self.client.post(token_verify_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
