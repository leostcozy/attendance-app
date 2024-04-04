from django.db import models
from django.contrib.auth.models import User
from attendance.models import Attendances
# Create your models here.

class WorkTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_time = models.DurationField(null=True)
    break_time = models.DurationField(null=True)
    

    def __str__(self):
        return self.user.username