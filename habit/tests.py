from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from habit.serializers import HabitSerializer
from users.models import User
from habit.models import Habit
from django.test import RequestFactory


class HabitTestCase(APITestCase):
    """Класс тестирования приложения Habit"""

    def setUp(self):
        self.factory = RequestFactory()
        # Создание пользователя с использованием email вместо username
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
        self.request.user = self.user  # Устанавливаем тестового пользователя в запрос
        # Создаем сериализатор с контекстом запроса
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

    def test_create_method(self):

        habit = self.serializer.create(self.valid_payload)
        self.assertIsInstance(habit, Habit)
        self.assertEqual(habit.owner, self.user)

    def test_validate_reward_and_conn_habit(self):
        data = {
            'reward': 'Reward',
            'conn_habit': 'Some other habit',
        }
        with self.assertRaises(ValidationError):
            self.serializer.validate(data)

    def test_validate_time_to_complete(self):
        # Проверяем, что возникает ошибка при времени выполнения больше 120 секунд
        data = {
            'time_to_complete': 130,  # Больше 120
        }
        with self.assertRaises(ValidationError):
            self.serializer.validate(data)

    def test_validate_conn_habit_sign(self):
        # Проверяем, что возникает ошибка, если связанная привычка не приятная
        conn_habit = Habit.objects.create(
            owner=self.user,
            place='Park',
            time='09:00',
            action='Walk',
            sign=False,  # Неприятная привычка
        )
        data = {
            'conn_habit': conn_habit,
        }
        with self.assertRaises(ValidationError):
            self.serializer.validate(data)

    def test_validate_sign_reward_and_conn_habit(self):
        # Проверяем, что возникает ошибка, если приятная привычка имеет вознаграждение
        data = {
            'sign': True,
            'reward': 'Reward',
        }
        with self.assertRaises(ValidationError):
            self.serializer.validate(data)

    def test_validate_periodicity(self):
        # Проверяем, что возникает ошибка, если периодичность вне допустимого диапазона
        data = {
            'periodicity': 0,  # Менее 1
        }
        with self.assertRaises(ValidationError):
            self.serializer.validate(data)

        data = {
            'periodicity': 8,  # Более 7
        }
        with self.assertRaises(ValidationError):
            self.serializer.validate(data)

    def test_validate_periodicity_not_empty(self):
        # Проверяем, что возникает ошибка, если периодичность не указана
        data = {}
        with self.assertRaises(ValidationError):
            self.serializer.validate(data)

    def test_validate_returns_data(self):
        """Тестируем, что валидные данные возвращаются корректно."""
        payload = {
            'place': 'Gym',
            'action': 'Workout',
            'sign': True,
            'periodicity': 3,
            'reward': None,
            'conn_habit': None,
            'time_to_complete': 60,
            'is_published': True,
        }

        serializer = HabitSerializer(data=payload, context={'request': self.request})

        # Проверяем, что данные валидные
        self.assertTrue(serializer.is_valid())

        # Теперь проверяем, что метод validate возвращает корректные данные
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['place'], payload['place'])
        self.assertEqual(validated_data['action'], payload['action'])
        self.assertEqual(validated_data['sign'], payload['sign'])
        self.assertEqual(validated_data['periodicity'], payload['periodicity'])
        self.assertEqual(validated_data['reward'], payload['reward'])
        self.assertEqual(validated_data['conn_habit'], payload['conn_habit'])
        self.assertEqual(validated_data['time_to_complete'], payload['time_to_complete'])
        self.assertEqual(validated_data['is_published'], payload['is_published'])
