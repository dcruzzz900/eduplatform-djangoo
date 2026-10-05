from django.urls import path

from . import views

app_name = 'dashboards'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('super-admin/', views.super_admin_dashboard, name='super_admin'),
    path('school-admin/', views.school_admin_dashboard, name='school_admin'),
    path('teacher/', views.teacher_dashboard, name='teacher'),
    path('student/', views.student_dashboard, name='student'),
    path('parent/', views.parent_dashboard, name='parent'),
]
