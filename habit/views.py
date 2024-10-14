from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Habit
from .paginations import CustomPagination
from .serializers import HabitSerializer, PublicHabitSerializer


class UserHabitViewSet(viewsets.ModelViewSet):
    """View set привычки текущего пользователя"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращает только привычки текущего пользователя
        return Habit.objects.filter(owner=self.request.user)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """View set публичных привычек"""

    serializer_class = PublicHabitSerializer
    pagination_class = CustomPagination
    queryset = Habit.objects.filter(
        is_published=True
    )  # Показываем все публичные привычки
    permission_classes = [AllowAny]  # Доступ для всех пользователей
