
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class User(AbstractUser):

    # is_student = models.BooleanField(default=False)
    # is_teacher = models.BooleanField(default=False)

    username = models.CharField(blank=True, null=True, max_length=50, unique=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=10)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    photo = models.ImageField(upload_to='uploads', blank=True)