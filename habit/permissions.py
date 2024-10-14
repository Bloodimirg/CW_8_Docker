from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Пользователь может редактировать и удалять только свои привычки."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsPublicOrOwner(permissions.BasePermission):
    """Пользователь может видеть публичные привычки или свои привычки."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Позволить всем доступ к публичным привычкам
        return (
            request.user.is_authenticated
        )  # Необходимо быть авторизованным для доступа к своим привычкам
