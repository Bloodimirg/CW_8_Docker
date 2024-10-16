from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""

    class Meta:
        model = User
        fields = ["id", "email", "password"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор получения токена access и refresh"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user.last_login = timezone.now()
        user.save()

        return token
