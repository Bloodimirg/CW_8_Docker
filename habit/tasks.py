import os
from datetime import timedelta

import requests
from celery import shared_task
from django.utils import timezone
from .models import Habit


@shared_task
def send_habit_reminders():
    """Проверка привычек и периодичности"""
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    # Получаем все привычки, которые нужно напомнить
    habits = Habit.objects.filter(
        owner__chat_id__isnull=False,
        is_published=True
    )

    for habit in habits:
        # Получаем все выполненные записи этой привычки за последние 7 дней
        completed_habits = habit.completedhabit_set.filter(date_completed__gte=one_week_ago)

        # Проверяем, выполнена ли привычка хотя бы один раз за последнюю неделю
        if completed_habits.exists() and habit.time_to_complete <= 120:
            # Привычка выполнена, проверяем периодичность
            if habit.periodicity < 7:
                message = (
                    f"Напоминание о привычке!\n"
                    f"Действие: {habit.action}\n"
                    f"Место: {habit.place}\n"
                    f"Время: {habit.time}\n"
                )
                send_telegram_message(habit.owner.chat_id, message)
        else:
            # Привычка не была выполнена за 7 дней
            message = (
                f"У вас не выполнена привычка за последнюю неделю!\n"
                f"Действие: {habit.action}\n"
            )
            send_telegram_message(habit.owner.chat_id, message)


def send_telegram_message(chat_id, message):
    """Отправка напоминания в телеграм"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    response = requests.post(url, json=payload)
    return response.json()
