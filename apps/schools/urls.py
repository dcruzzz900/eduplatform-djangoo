from django.urls import path

from . import views

app_name = 'schools'

urlpatterns = [
    path('schools/', views.school_list, name='list'),
    path('schools/new/', views.school_create, name='create'),
    path('schools/<int:pk>/', views.school_detail, name='detail'),
]
