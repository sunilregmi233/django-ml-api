# disaster_recording/views.py

# disaster_recording/views.py

from rest_framework import viewsets
from .models import Disaster
from .serializers import DisasterSerializer
from users.permissions import IsLoggedInUserOrAdmin, IsAdminUser


class DisasterViewSet(viewsets.ModelViewSet):
    permission_classes = (IsLoggedInUserOrAdmin,)
    queryset = Disaster.objects.all()
    serializer_class = DisasterSerializer
