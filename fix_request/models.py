from django.db import models
from django.contrib.auth.models import User
from attendance.models import Attendances

# Create your models here.

class AttendanceFixRequests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    attendance = models.ForeignKey(Attendances, on_delete=models.CASCADE, null=True)
    reason = models.CharField(max_length=255) # 申請理由
    stamp_type = models.CharField( # 申請種別
        max_length = 2,
        choices = [
            ('AT', 'attendance'),
            ('LE', 'leave'),
        ]
    )
    is_accepted = models.BooleanField(default=False) # 承認されたか
    revision_time = models.DateTimeField() # 修正希望時間
    request_time = models.DateTimeField(auto_now_add=True) # 申請時間
    checked_time = models.DateTimeField(null=True) # 確認時間

