from django.urls import path
from .views import (
    FixAttendanceRequestView,
    AttendanceAcceptionView
)

urlpatterns = [
    path('request', FixAttendanceRequestView.as_view(), name='fix_request'),
    path('acception/', AttendanceAcceptionView.as_view(), name='fix_acception'),
]
