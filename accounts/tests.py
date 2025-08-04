from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User, VerificationOtp
from accounts.utils import generate_otp_code

class TestUserRegisterView(APITestCase):
    def setUp(self):
        pass

    def test_happy(self):
        url = reverse('register')
        data = {
            'first_name': 'testname',
            'last_name': 'testlastname',
            'email': 'T9BZ3@example.com',
            'password': 'testpass'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.data['first_name'], 'testname')
        self.assertEqual(response.status_code, 201)

class TestVerifyOtpView(APITestCase):
    def setUp(self):
        self.new_user = User.objects.create(
            first_name='testname',
            last_name='testlastname',
            email='T9BZ3@example.com',
            is_active=False
        )
        self.new_user.set_password('testpass')
        self.new_user.save()
        self.otp_code = generate_otp_code()
        self.verification = VerificationOtp.objects.create(
            user=self.new_user,
            code=self.otp_code,
            type='register',
            expires_in=timezone.now() + timedelta(minutes=5),
            is_active=True
        )

    def test_happy(self):
        url = reverse('verify-otp')
        data = {
            'email': self.new_user.email,
            'code': self.otp_code,
            'verify_type': 'register'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'otp_code_activated')

    def test_otp_code_not_found(self):
        url = reverse('verify-otp')
        data = {
            'email': self.new_user.email,
            'code': 999999,  # noto'g'ri kod
            'verify_type': 'register'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'otp_code_not_found')

    def test_otp_already_activated(self):
        self.verification.is_active = False
        self.verification.save()

        url = reverse('verify-otp')
        data = {
            'email': self.new_user.email,
            'code': self.otp_code,
            'verify_type': 'register'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'otp_code_already_activated')

    def test_otp_expired(self):
        self.verification.expires_in = timezone.now() - timedelta(minutes=1)
        self.verification.save()

        url = reverse('verify-otp')
        data = {
            'email': self.new_user.email,
            'code': self.otp_code,
            'verify_type': 'register'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'otp_code_expired')

    def test_user_does_not_exist(self):
        url = reverse('verify-otp')
        data = {
            'email': 'wrong@example.com',  # noto'g'ri email
            'code': self.otp_code,
            'verify_type': 'register'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 500)  # APIException -> 500 chiqadi
        self.assertIn('User does not exist', str(response.data))
