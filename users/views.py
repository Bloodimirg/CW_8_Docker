from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer


class UserCreateApiView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Получение пары токенов access/refresh"""

    serializer_class = CustomTokenObtainPairSerializer
