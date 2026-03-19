"""
Tests for the api in the user app.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

USER_URL = reverse('user:user-list')

class PublicUserApiTests(TestCase):
    """Tests for user endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='original@example.com',
            password='password123',
            name='Original Name'
        )
        self.detail_url = reverse('user:user-detail', args=[self.user.id])
        self.client.force_authenticate(user=self.user)

    def test_create_user_success(self):
        """Test creating a new user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test Name',
        }
        res = self.client.post(USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])

        self.assertEqual(user.name, payload['name'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test user cant be created with email that already exists."""
        payload = {'email': 'test@example.com', 'password': 'password123', 'name': 'Name'}
        get_user_model().objects.create_user(**payload)

        res = self.client.post(USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password isnt too short."""
        payload = {'email': 'test@example.com', 'password': '123', 'name': 'Name'}
        res = self.client.post(USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', res.data)

    def test_partial_update_name(self):
        """Test the field sent has changed."""
        payload = {'name': 'New Name'}
        res = self.client.patch(self.detail_url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.email, 'original@example.com')

    def test_update_password_is_hashed(self):
        """Test the password is hashed."""
        new_password = 'new_password_123'
        payload = {'password': new_password}
        res = self.client.patch(self.detail_url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password(new_password))

    def test_full_update_with_put(self):
        """Test PUT updates all fields."""
        payload = {
            'email': 'newemail@example.com',
            'name': 'Full Update Name',
            'password': 'newpassword123'
        }
        res = self.client.put(self.detail_url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload['email'])
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))

    def test_delete_user(self):
        """Test will deactivate user."""
        user = get_user_model().objects.create_user(
            email='delete_me@example.com',
            password='password123',
            name='To Be Deleted'
        )
        url = reverse('user:user-detail', args=[user.id])
        
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        
        user.refresh_from_db()
        
        self.assertFalse(user.is_active)
        self.assertTrue(get_user_model().objects.filter(id=user.id).exists())
