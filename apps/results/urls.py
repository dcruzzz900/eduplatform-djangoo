from django.urls import path

from . import views

app_name = 'results'

urlpatterns = [
    path('entry/', views.results_entry, name='entry'),
    path('manage/', views.results_manage, name='manage'),
    path('my/', views.my_results, name='my'),
    path('report/<int:student_id>/', views.report_card, name='report_card'),
]
