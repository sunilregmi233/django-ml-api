# disaster_recording/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisasterViewSet
from .views import google_login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'disasters', DisasterViewSet, basename='disaster')

urlpatterns = [
    path('', include(router.urls)),
    path('google-login/', csrf_exempt(google_login), name='google-login'),
]
# Add this at the end to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)