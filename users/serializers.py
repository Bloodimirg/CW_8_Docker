from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])  # Хешируем пароль
        user.is_active = True  # Устанавливаем пользователя активным
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор получения токена access и refresh"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        user.last_login = timezone.now()
        user.save()

        return token
