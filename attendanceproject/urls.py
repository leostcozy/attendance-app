from django.contrib import admin
from django.urls import path, include

admin.site.site_title = "JobAt 管理者サイト"
admin.site.site_header = "JobAt 管理者サイト"
admin.site.index_title = "メニュー"
admin.site.disable_action("delete_selected")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    path("", include("attendance.urls")),
    path("fix_request/", include("fix_request.urls")),
    path("workhour/", include("workhour.urls")),
]
