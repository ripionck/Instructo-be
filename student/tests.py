from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Student
from django.core import mail


class StudentAPITests(APITestCase):
    def setUp(self):
        # Create test user and student
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.student = Student.objects.create(
            user=self.user,
            gender='M',
            mobile='1234567890'
        )
        self.token = Token.objects.create(user=self.user)

    def test_student_filter_viewset(self):
        # Test unauthenticated access
        response = self.client.get(reverse('student-profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test authenticated access
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse('student-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_student_registration(self):
        registration_data = {
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'Student'
        }

        response = self.client.post(
            reverse('student-register'),
            registration_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)  # Verify email was sent

    def test_student_login(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }

        response = self.client.post(
            reverse('student-login'),
            login_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('student_id', response.data)

    def test_student_logout(self):
        # Login first
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(reverse('student-logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify token is deleted
        self.assertFalse(
            Token.objects.filter(user=self.user).exists()
        )

    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        password_data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'confirm_password': 'newpass123'
        }

        response = self.client.put(
            reverse('change-password'),
            password_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_class_filter(self):
        response = self.client.get(
            reverse('class-filter'),
            {'tuition_class': 'class_10'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StudentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            gender='M',
            mobile='1234567890'
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.student),
            f"{self.user.first_name} {self.user.last_name}"
        )

    def test_get_full_name(self):
        self.assertEqual(
            self.student.get_full_name(),
            f"{self.user.first_name} {self.user.last_name}"
        )
