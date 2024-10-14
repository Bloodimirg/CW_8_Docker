from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserHabitViewSet, PublicHabitViewSet

router = DefaultRouter()
router.register(r"my-habits", UserHabitViewSet, basename="my-habits")
router.register(r"public-habits", PublicHabitViewSet, basename="public-habits")

app_name = "habit"

urlpatterns = [
    path("", include(router.urls)),
]
