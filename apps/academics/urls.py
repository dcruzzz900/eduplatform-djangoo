from django.urls import path

from . import views

app_name = 'academics'

urlpatterns = [
    path('classes/', views.class_list, name='classes'),
    path('subjects/', views.subject_list, name='subjects'),
    path('students/', views.student_list, name='students'),
    path('students/enrol/', views.student_enrol, name='student_enrol'),
]
