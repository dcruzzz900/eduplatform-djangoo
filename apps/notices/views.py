from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.notices.models import Notice


@login_required
def notice_list(request):
    school = request.user.school
    if not school:
        return redirect('dashboards:home')
    notices = Notice.objects.filter(school=school)
    if request.method == 'POST':
        Notice.objects.create(
            school=school,
            title=request.POST.get('title', '').strip(),
            body=request.POST.get('body', '').strip(),
            audience=request.POST.get('audience', 'ALL'),
            priority=request.POST.get('priority', 'NORMAL'),
            is_published=True,
            published_at=timezone.now(),
            created_by=request.user,
        )
        messages.success(request, 'Notice published.')
        return redirect('notices:list')
    return render(request, 'notices/list.html', {'notices': notices})
