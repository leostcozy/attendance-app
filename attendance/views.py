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
        push_type = request.POST.get('push_type')
        # 出勤しているかを調べる
        is_attendanced = Attendances.objects.filter(
            user = request.user,
            attendance_time__date=datetime.now().date()
        ).exists()
        # 休憩中か調べる
        is_break_started = Attendances.objects.filter(
            user = request.user,
            break_start_time__date=date.today()
        ).exists()
        # 休憩終了したか調べる
        is_break_end = Attendances.objects.filter(
            user = request.user,
            break_end_time__date=date.today()
        ).exists()
        # 退勤しているかを調べる
        is_left = Attendances.objects.filter(
            user = request.user,
            leave_time__date = date.today()
        ).exists()

        response_body = {}
        if push_type == 'attendance' and not is_attendanced: # 出勤ボタンが押された時かつ今日の出勤データがない場合
            # 出勤したユーザーをDBに保存する
            attendance = Attendances(user=request.user)
            attendance.save()
            response_time = attendance.attendance_time
            response_body = {
                "result": "success",
                "attendance_time": response_time.strftime('%Y-%m-%d %H:%M:%S')
            }
        elif push_type == 'break_start' and not is_break_started and is_attendanced: # 休憩開始ボタンが押された時かつ今日の休憩データがない時かつ今日の出勤データがある場合
            # 休憩開始時間を更新する
            attendance = Attendances.objects.filter(
                user=request.user,
                attendance_time__date= date.today()
            )[0]
            attendance.break_start_time = datetime.now()
            attendance.save()
            response_body = {
                "result": "break_start_success",
                "break_start_time": attendance.break_start_time.strftime('%Y-%m-%d %H:%M:%S')
            }
        elif push_type == 'break_end' and not is_break_end and is_break_started: # 休憩終了ボタンが押された時かつ、今日の休憩終了データがない時かつ、今日の休憩開始データがある場合
            # 休憩終了時間を更新する
            attendance = Attendances.objects.filter(
                user=request.user,
                break_start_time__date= date.today()
            )[0]
            attendance.break_end_time = datetime.now()
            attendance.save()
            response_body = {
                "result": "break_end_success",
                "break_end_time": attendance.break_end_time.strftime('%Y-%m-%d %H:%M:%S')
            }
        elif push_type == 'leave' and not is_left: # 退勤ボタンが押された時かつ今日の退勤データがない場合
            if is_attendanced:
                # 退勤するユーザーのレコードの退勤時間を更新する
                attendance = Attendances.objects.filter(
                    user=request.user,
                    attendance_time__date= date.today()
                )[0]
                attendance.leave_time = datetime.now()
                attendance.save()
                response_time = attendance.leave_time
                response_body = {
                    "result": "success",
                    "leave_time": response_time.strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                response_body = {
                    "result": "not_attended"
                }
        if not response_body:
            response_body = {
                "result": "already_exists"
            }
        return JsonResponse(response_body)
        
class AttendanceRecords(LoginRequiredMixin, TemplateView):
    template_name = 'attend_records.html'
    login_url = '/accounts/login/'
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        # search_year = today.year
        # search_month = today.month
        # リクエストパラメータを受け取る
        search_param = request.GET.get('year_month')
        if search_param:
            search_params = list(map(int, search_param.split('-')))
            search_year = search_params[0]
            search_month = search_params[1]
        else:
            search_year = today.year
            search_month = today.month
        
        # 年と月で絞り込み
        month_attandances =Attendances.objects.filter(
            user = request.user,
            attendance_time__year = search_year,
            attendance_time__month = search_month
        ).order_by('attendance_time')

        # context用のデータに整形
        attendances_context =[]
        for attendance in month_attandances:
            attendance_time = attendance.attendance_time
            leave_time = attendance.leave_time
            if leave_time:
                leave_time = leave_time.strftime('%H:%M:%S')
            else:
                if attendance_time.date() == today.date():
                    leave_time = None
                else:
                    leave_time = 'not_pushed'
            day_attendance = {
                'date': attendance_time.strftime('%Y-%m-%d'),
                'attendance_at': attendance_time.strftime('%H:%M:%S'),
                'leave_at': leave_time
                }
            attendances_context.append(day_attendance)
        
        context = {'attendances': attendances_context}
        # Templateにcontextを含めてレスポンスを返す
        return self.render_to_response(context)

