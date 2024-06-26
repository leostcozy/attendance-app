from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Attendances(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance_time = models.DateTimeField(default=datetime.now) # 出勤時間
    leave_time = models.DateTimeField(null=True) # 退勤時間
    break_start_time = models.DateTimeField(null=True, blank=True)  # 休憩開始時間
    break_end_time = models.DateTimeField(null=True, blank=True) # 休憩終了時間
    
    
    def __str__(self):
        return self.user.username