from django.urls import path

from .views import AppLoginView, logout_view

app_name = 'accounts'

urlpatterns = [
    path('login/', AppLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
