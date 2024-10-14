from django.contrib import admin

from users.models import User


@admin.register(User)
class LessonAdmin(admin.ModelAdmin):
    """Админка уроков"""
    list_display = ("pk", "username", "email", "chat_id")
