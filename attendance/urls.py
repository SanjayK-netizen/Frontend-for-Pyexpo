from django.contrib import admin
from django.urls import path
from attendance import views   # replace 'myapp' with your app name

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL → login page
    path('', views.user_login, name='login'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Face recognition attendance
    path('face_punch/', views.face_punch, name='face_punch'),

    # Attendance spotline
    path('attendance_spotline/', views.attendance_spotline, name='attendance_spotline'),

    # Optional: alias /home → dashboard
    path('home/', views.dashboard, name='home'),

    # Django auth redirect alias
    path('accounts/login/', views.user_login, name='accounts-login'),
]