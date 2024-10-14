from django.db import models
from django.utils import timezone

from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    CHOICES_PERIOD = (("daily", "Ежедневная"), ("weekly", "Еженедельная"),)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, **NULLABLE, verbose_name="Создатель"
    )
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(default=timezone.now(), verbose_name="Время")
    action = models.CharField(max_length=100, verbose_name="Действие")
    sign = models.BooleanField(default=True, verbose_name="Признак приятной привычки")
    conn_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, **NULLABLE, verbose_name="Связанная привычка"
    )
    periodicity = models.PositiveIntegerField(
        default=7,
        validators=[MinValueValidator(7), MaxValueValidator(365)],
        verbose_name="Периодичность",
    )
    reward = models.CharField(max_length=100, **NULLABLE, verbose_name="Вознаграждение")
    time_to_complete = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name="Время на выполнение",
    )
    is_published = models.BooleanField(default=True, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
