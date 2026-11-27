from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase


class UserRegistrationTests(APITestCase):
    def test_register_user(self):
        payload = {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'strongpass123',
            'phone': '+79991234567',
        }

        response = self.client.post(reverse('register'), payload, format='json')

        self.assertEqual(response.status_code, 201)
        user = get_user_model().objects.get(username='alice')
        self.assertEqual(user.email, payload['email'])
        self.assertEqual(user.phone, payload['phone'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertIn('username', response.data)
        self.assertIn('phone', response.data)
