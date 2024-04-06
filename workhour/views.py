from datetime import datetime
from .models import Attendances, WorkTime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from datetime import timedelta

class WorkTimeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'work_time.html'
    login_url = '/accounts/login/'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get(self, request, *args, **kwargs):
        # リクエストから年月を取得
        search_param = request.GET.get('year_month')
        if search_param:
            search_params = list(map(int, search_param.split('-')))
            search_year = search_params[0]
            search_month = search_params[1]
        else:
            today = datetime.today()
            search_year = today.year
            search_month = today.month

        # 年と月で絞り込み
        attendances = Attendances.objects.filter(
            attendance_time__year=search_year,
            attendance_time__month=search_month
        )

        # 勤務時間を計算し、結果を辞書に保存
        work_times = {}
        for attendance in attendances:
            if attendance.leave_time and attendance.attendance_time: # 出勤時間と退勤時間がある場合
                # 勤務時間（退勤時間 - 出勤時間）を計算
                work_time = attendance.leave_time - attendance.attendance_time
                # ユーザーごとに勤務時間を集計
                work_time_obj, created = WorkTime.objects.get_or_create(
                    user=attendance.user,
                    defaults={'work_time': timedelta(), 'break_time': timedelta()}
                )
                if created:
                    # 新規作成された場合、計算した勤務時間を設定
                    work_time_obj.work_time = work_time
                

                work_time_obj.save()  # 変更をデータベースに保存

                # 辞書にはユーザー名をキーとしてWorkTimeインスタンスを格納
                work_times[attendance.user.username] = work_time_obj
        # 結果をテンプレートに渡す
        context = {
            'work_times': work_times,
        }
        return self.render_to_response(context)