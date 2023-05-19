"""
Tests for the django admin site
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password='1234QWer!',
            username='admin',
        )
        self.client.force_login(self.admin)
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password='1234QWer!',
            username='user',
        )
        return super().setUp()
    
    def test_users_list(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)

    def test_users_list(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
    
    def test_users_create(self):
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
