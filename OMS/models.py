# Create your models here.
from django.db import models
from users.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return self.user.get_full_name()

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee}: {self.check_in.strftime('%Y-%m-%d %H:%M:%S')}"