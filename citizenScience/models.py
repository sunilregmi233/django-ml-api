from django.db import models
from users.models import User
from allauth.socialaccount.models import SocialAccount


class Disaster(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='disaster_videos/')
    date_reported = models.DateTimeField(auto_now_add=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
