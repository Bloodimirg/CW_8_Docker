from rest_framework.test import APITestCase

from habit.serializers import HabitSerializer
from users.models import User
from habit.models import Habit
from django.test import RequestFactory
from rest_framework.exceptions import ValidationError


class HabitTestCase(APITestCase):
    """Класс тестирования приложения Habit"""

    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create(
            email="testuser@example.com",
            password="testpassword"
        )

        # Создание тестовой привычки
        self.habit = Habit.objects.create(
            owner=self.user,
            place="Gym",
            time="08:00",
            action="Workout",
            sign=True,
            periodicity=3,
            reward="Protein shake",
            time_to_complete=60,
            is_published=True,
        )

        self.valid_payload = {
            'place': 'Gym',
            'time': '08:00',
            'action': 'Workout',
            'sign': True,
            'periodicity': 3,
            'reward': "Protein shake",
            'time_to_complete': 60,
            'is_published': True,
        }
        self.request = self.factory.post('/dummy-url/')
        self.request.user = self.user
        self.serializer = HabitSerializer(data=self.valid_payload, context={'request': self.request})

    def test_create_habit(self):
        """Тест на создание привычки"""
        habit_count = Habit.objects.count()
        self.assertEqual(habit_count, 1, "Привычка должна быть успешно создана")

    def test_update_habit(self):
        """Тест на обновление привычки"""
        new_action = "Exercise"
        self.habit.action = new_action
        self.habit.save()

        self.assertEqual(self.habit.action, new_action, "Привычка должна быть обновлена")

    def test_periodicity_habit(self):
        """Тест на периодичность выполнения привычки"""
        self.assertEqual(self.habit.periodicity, 3, "Периодичность должна быть установлена на 3")

    def test_habit_owner(self):
        """Тест на проверку владельца привычки"""
        self.assertEqual(self.habit.owner, self.user, "Владелец привычки должен совпадать "
                                                      "с тестовым пользователем")

    def test_habit_publish_status(self):
        """Тест на публичный статус привычки"""
        self.assertTrue(self.habit.is_published, "Привычка должна быть опубликована")

    def test_validate_periodicity_not_empty(self):
        """Тест, что возникает ошибка, если периодичность не указана"""
        data = {}
        with self.assertRaises(ValidationError):
            self.serializer.validate(data)

    def test_valid_periodicity(self):
        """Тест валидной периодичности (от 1 до 7)"""
        # Убираем вознаграждение, так как это приятная привычка
        valid_payload = {
            'place': 'Gym',
            'time': '08:00',
            'action': 'Workout',
            'sign': True,  # Приятная привычка
            'periodicity': 3,
            'time_to_complete': 60,
            'is_published': True,
            'reward': None,  # Убираем вознаграждение, чтобы пройти проверку
        }

        serializer = HabitSerializer(data=valid_payload, context={'request': None})
        self.assertTrue(serializer.is_valid(), f"Сериализатор должен быть валиден. Ошибки: {serializer.errors}")

    def test_reward_and_conn_habit_error(self):
        """Тест на проверку ошибки при указании вознаграждения, и связанной привычки одновременно"""
        # Создаем связанную привычку
        related_habit = Habit.objects.create(
            owner=self.user,
            place="Home",
            time="10:00",
            action="Reading",
            sign=True,  # Приятная привычка
            periodicity=1,
            is_published=True,
        )

        # Формируем неправильные данные (оба поля указаны)
        invalid_payload = {
            'place': 'Gym',
            'time': '08:00',
            'action': 'Workout',
            'sign': False,
            'periodicity': 3,
            'reward': "Protein shake",  # Указано вознаграждение
            'conn_habit': related_habit.id,  # Указана связанная привычка
            'time_to_complete': 60,
            'is_published': True,
        }

        # Создаем сериализатор с неправильными данными
        serializer = HabitSerializer(data=invalid_payload, context={'request': None})

        # Проверяем, что сериализатор не валиден
        self.assertFalse(serializer.is_valid(),
                         "Сериализатор не должен быть валиден, если указаны и вознаграждение, и связанная привычка")

        # Проверяем, что ошибка валидации содержит нужное сообщение
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Нельзя указывать и вознаграждение, и связанную привычку одновременно. Выберите одно.",
            "Должна быть ошибка валидации, если указаны и вознаграждение, и связанная привычка"
        )
