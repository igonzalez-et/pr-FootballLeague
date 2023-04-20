from django.contrib import admin
from django.urls import include, path

from laLliga import views

from laLliga.views import *
from django.contrib.auth.views import PasswordChangeDoneView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('laLliga/',include('laLliga.urls')),
    path("accounts/profile/", profile, name="profile"),
    path('accounts/password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path("accounts/", include("django.contrib.auth.urls")),

]