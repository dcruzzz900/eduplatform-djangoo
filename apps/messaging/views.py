from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.models import User
from apps.messaging.models import Message


@login_required
def inbox(request):
    school = request.user.school
    if not school:
        return redirect('dashboards:home')
    inbox_qs = Message.objects.filter(school=school, recipient=request.user).select_related('sender')
    sent_qs = Message.objects.filter(school=school, sender=request.user).select_related('recipient')
    directory = User.objects.filter(school=school, is_active=True).exclude(pk=request.user.pk)

    if request.method == 'POST':
        rid = request.POST.get('recipient_id')
        body = request.POST.get('body', '').strip()
        recipient = User.objects.filter(school=school, pk=rid).first()
        if recipient and body:
            Message.objects.create(
                school=school,
                sender=request.user,
                recipient=recipient,
                subject=request.POST.get('subject', '').strip(),
                body=body,
            )
            messages.success(request, 'Message sent.')
            return redirect('messaging:inbox')
        messages.error(request, 'Recipient and body required.')

    return render(
        request,
        'messaging/inbox.html',
        {'inbox': inbox_qs[:50], 'sent': sent_qs[:50], 'directory': directory},
    )
