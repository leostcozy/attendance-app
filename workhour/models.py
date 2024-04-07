from django.db import models
from django.contrib.auth.models import User
from attendance.models import Attendances
from datetime import datetime

# Create your models here.

class WorkTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField(default= datetime.now().year)  
    month = models.IntegerField(default= datetime.now().month)
    work_time = models.DurationField(null=True)
    break_time = models.DurationField(null=True)
    actual_work_time = models.DurationField(null=True)  # 実際の勤務時間（休憩時間を引いた時間）
    
    def format_duration(self, duration):
        if duration:
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return '{}時間{}分{}秒'.format(hours, minutes, seconds)
        return "未設定"

    def work_time_format(self):
        return self.format_duration(self.work_time)

    def break_time_format(self):
        return self.format_duration(self.break_time)
    
    def actual_work_time_format(self):
        return self.format_duration(self.actual_work_time)

    def __str__(self):
        return self.user.username
    
    