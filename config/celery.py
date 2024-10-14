from __future__ import absolute_import, unicode_literals
from celery import Celery
import os


# Загрузка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Настройки Celery из переменных окружения
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()
