from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.accounts.models import OTPDevice

User = get_user_model()


class AccountsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.phone = '01711112222'

    def test_send_otp(self):
        response = self.client.post('/api/auth/otp/send/', {'phone': self.phone}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertTrue(OTPDevice.objects.filter(phone=self.phone).exists())

    def test_verify_otp_success(self):
        # Send OTP first
        self.client.post('/api/auth/otp/send/', {'phone': self.phone}, format='json')
        
        response = self.client.post('/api/auth/otp/verify/', {'phone': self.phone, 'otp': '1234'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['phone'], self.phone)
        self.assertTrue(User.objects.filter(phone=self.phone).exists())

    def test_verify_otp_invalid_code(self):
        response = self.client.post('/api/auth/otp/verify/', {'phone': self.phone, 'otp': '9999'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
