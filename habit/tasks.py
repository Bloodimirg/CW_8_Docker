import os

import requests
from celery import shared_task
from django.utils import timezone
from .models import Habit


@shared_task
def send_habit_reminders():
    """Проверка привычек и периодичности"""
    now = timezone.now()

    habits = Habit.objects.filter(
        is_published=True,
    )

    for habit in habits:
        if habit.owner.chat_id and habit.time <= now:
            message = (
                f"Напоминание о привычке!\n"
                f"Действие: {habit.action}\n"
                f"Место: {habit.place}\n"
                f"Время: {habit.time}\n"
                f"Вознаграждение: {habit.reward if habit.reward else 'Нет'}\n"
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
