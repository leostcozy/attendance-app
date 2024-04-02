from django.urls import path
from .views import HomeView, PushTimecardView, AttendanceRecords

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("push/", PushTimecardView.as_view(), name="push"),
    path("records/", AttendanceRecords.as_view(), name="records")
]

