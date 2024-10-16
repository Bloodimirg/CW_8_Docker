from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.permissions import IsModerator, IsOwner
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

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModerator,)  # создавать могут не модераторы
        elif self.action in ['update', 'retrieve', 'partial_update']:
            self.permission_classes = (IsModerator | IsOwner,)  # обновлять может модератор или владелец
        elif self.action == 'destroy':
            self.permission_classes = (~IsModerator | IsOwner,)  # удалять может не модератор или владелец
        return super().get_permissions()


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """View set публичных привычек"""

    serializer_class = PublicHabitSerializer
    pagination_class = CustomPagination
    queryset = Habit.objects.filter(
        is_published=True
    )  # Показываем все публичные привычки
    permission_classes = [AllowAny]  # Доступ для всех пользователей
