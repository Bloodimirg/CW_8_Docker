from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("habit/", include("habit.urls", namespace="habit")),
    path("users/", include("users.urls", namespace="users")),
]
