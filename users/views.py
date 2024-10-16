from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer


class UserCreateApiView(CreateAPIView):
    """Создание пользователя"""
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        chat_id = self.request.data.get('chat_id')
        user = serializer.save(is_active=True, chat_id=chat_id)
        user.set_password(user.password)
        user.save()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Получение пары токенов access/refresh"""

    serializer_class = CustomTokenObtainPairSerializer
