from django.urls import path
from .views import HabitCreateView, HabitListView

app_name = 'habit'  # Добавь это

urlpatterns = [
    path('', HabitListView.as_view(), name='habit-list'),  # Например, список привычек
    path('create/', HabitCreateView.as_view(), name='habit-create'),  # Создание привычки
]
