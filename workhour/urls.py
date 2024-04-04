from django.urls import path
from .views import WorkTimeView


urlpatterns = [
    path('worktime/', WorkTimeView.as_view(), name='work_time'),
]

