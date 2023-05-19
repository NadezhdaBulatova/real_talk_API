"""Test for models"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test models"""
    def test_create_user_with_email_success(self):
        """Successful set up of the user account with email"""
        email='test@example.com'
        password='1234QWer!'
        username='user'
        user = get_user_model().objects.create_user(
            email=email, password=password, username=username
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        """Test email of the new user to be normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAmPLE.com', 'Test2@example.com'],
            ['TEST3@example.com', 'TEST3@example.com'],
            ['TEST4@Example.COM', 'TEST4@example.com'],
        ]
        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email, f'username{email}', '1234QWer!')
            self.assertEqual(user.email, expected_email)
    
    def test_create_user_failed(self):
        """Test create user fails if email or username is not provided"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', username='username', password='1234QWer!')
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='user@example.com', username='', password='1234QWer!')

    def test_create_superuser(self):
        """Test create superuser"""
        superuser = get_user_model().objects.create_superuser('test@example.com', 'superuser', '1234QWer!')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)