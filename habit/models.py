from django.db import models
from django.utils import timezone
from config.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


def get_current_time():
    return timezone.now().time()


class Habit(models.Model):
    """Модель привычки"""

    CHOICES_PERIOD = (
        (1, "Ежедневная"),
        (7, "Еженедельная"),
    )

    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name="Создатель"
    )
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(default=get_current_time, verbose_name="Время")
    action = models.CharField(max_length=100, verbose_name="Действие")
    sign = models.BooleanField(default=True, verbose_name="Признак приятной привычки")
    conn_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, **NULLABLE, verbose_name="Связанная привычка"
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность",
    )
    reward = models.CharField(max_length=100, **NULLABLE, verbose_name="Вознаграждение")
    time_to_complete = models.PositiveIntegerField(
        default=120,
        verbose_name="Время на выполнение",
    )
    is_published = models.BooleanField(default=True, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
