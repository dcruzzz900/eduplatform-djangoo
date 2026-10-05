"""Serve service worker and offline page at site root (required for PWA scope)."""
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from pathlib import Path

from django.conf import settings


@require_GET
@never_cache
def service_worker(request):
    # Prefer static/js/sw.js content; serve with correct JS content-type
    path = Path(settings.BASE_DIR) / 'static' / 'js' / 'sw.js'
    body = path.read_text(encoding='utf-8') if path.exists() else '/* missing sw */'
    response = HttpResponse(body, content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache'
    return response


@require_GET
def offline_page(request):
    return render(request, 'base/offline.html')
