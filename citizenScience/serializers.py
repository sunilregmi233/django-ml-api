# disaster_recording/serializers.py

from rest_framework import serializers
from .models import Disaster
# from allauth.socialaccount.models import SocialAccount, SocialToken


class DisasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disaster
        fields = '__all__'

