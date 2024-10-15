from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateApiViewTestCase(APITestCase):
    """Тестирование представления создания пользователя"""

    def setUp(self):
        # Создание тестового пользователя
        self.existing_user = User.objects.create(
            email="existinguser@example.com",
            password="testpassword"
        )

        # URL для тестирования
        self.url = reverse('users:register')

        # Валидные данные для создания пользователя
        self.valid_payload = {
            'email': 'newuser@example.com',
            'password': 'strong_password_123',
        }

    def test_create_user_valid(self):
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.valid_payload['email']).exists())

    def test_str_method(self):
        # Проверяем, что метод __str__() возвращает правильное значение
        self.assertEqual(str(self.existing_user), "existinguser@example.com")
