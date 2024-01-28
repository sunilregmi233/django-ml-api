# disaster_recording/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisasterViewSet
from .views import google_login
from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()
router.register(r'disasters', DisasterViewSet, basename='disaster')

urlpatterns = [
    path('', include(router.urls)),
    path('google-login/', csrf_exempt(google_login), name='google-login'),
]
