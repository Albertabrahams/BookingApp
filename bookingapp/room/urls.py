from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet

router = DefaultRouter()
router.register(r'Room', RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
