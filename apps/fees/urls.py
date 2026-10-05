from django.urls import path

from . import views

app_name = 'fees'

urlpatterns = [
    path('', views.fees_admin, name='admin'),
    path('parent/', views.fees_parent, name='parent'),
]
