from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Attendances
from datetime import date, datetime

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    # ログインがされてなかったらリダイレクトされるURL
    login_url = '/accounts/login/'

class PushTimecardView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    def post(self, request, *args, **kwargs):
        push_type = request.POST.get['push_type']

        is_attendance = Attendances.objects.filter(
            user=request.user, 
            attendance_time__date=datetime.now().date()
        ).exists()

        response_body = {}
        if push_type == 'attendance':
            # 出勤したユーザーをDBに保存する
            attendance = Attendances(user=request.user)
            attendance.save()
            response_time = attendance.attendance_time
            response_body = {
                'result': 'success',
                'leave_time': response_time.strftime('%Y-%m-%d %H:%M:%S')
            }
        elif push_type == 'leave':
            if is_attendance:
                # 退勤するユーザーのレコードの退勤時間を更新する
                attendance = Attendances.objects.filter(
                    user=request.user,
                    attendance_time__date= date.today()
                )[0]
                attendance.leave_time = datetime.now()
                attendance.save()
                response_time = attendance.leave_time
                response_body = {
                    'result': 'success',
                    'leave_time': response_time.strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                response_body = {
                    'result': 'error',
                    'message': 'Not attendance'
                }
        if not response_body:
            response_body = {
                'result': 'already_exists'
            }
        return JsonResponse(response_body)
        

