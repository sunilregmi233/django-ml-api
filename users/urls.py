from django.urls import path, include
from rest_framework import routers
from users.views import UserViewSet, UserProfileViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('user-profile', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]