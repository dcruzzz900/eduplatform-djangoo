from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.pwa_views import service_worker, offline_page

urlpatterns = [
    path('sw.js', service_worker, name='service_worker'),
    path('offline/', offline_page, name='offline'),
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('', include('apps.schools.urls')),
    path('academics/', include('apps.academics.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('results/', include('apps.results.urls')),
    path('fees/', include('apps.fees.urls')),
    path('notices/', include('apps.notices.urls')),
    path('messages/', include('apps.messaging.urls')),
    path('', include('apps.accounts.dashboard_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
