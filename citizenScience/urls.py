# disaster_recording/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisasterViewSet

router = DefaultRouter()
router.register(r'disasters', DisasterViewSet, basename='disaster')

urlpatterns = [
    path('', include(router.urls)),
]
