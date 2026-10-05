import secrets
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.academics.models import Student
from apps.fees.models import FeeInvoice, FeeItem, FeePayment


@login_required
def fees_admin(request):
    school = request.user.school
    if not school:
        return redirect('dashboards:home')
    items = FeeItem.objects.filter(school=school)
    invoices = FeeInvoice.objects.filter(school=school).select_related('student')[:50]

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_item':
            FeeItem.objects.create(
                school=school,
                name=request.POST.get('name', '').strip(),
                amount=request.POST.get('amount') or 0,
            )
            messages.success(request, 'Fee item added.')
        elif action == 'generate':
            item_ids = request.POST.getlist('fee_items')
            fee_items = FeeItem.objects.filter(school=school, id__in=item_ids)
            total = sum(float(i.amount) for i in fee_items)
            students = Student.objects.filter(school=school, status='ACTIVE')
            n = 0
            for st in students:
                ref = f'INV-{int(time.time())}-{secrets.token_hex(2).upper()}'
                inv = FeeInvoice.objects.create(
                    school=school,
                    student=st,
                    reference=ref,
                    total_amount=total,
                    amount_paid=0,
                    balance=total,
                )
                n += 1
            messages.success(request, f'Generated {n} invoice(s).')
        elif action == 'pay':
            inv_id = request.POST.get('invoice_id')
            amount = float(request.POST.get('amount') or 0)
            inv = FeeInvoice.objects.filter(school=school, pk=inv_id).first()
            if inv and amount > 0:
                FeePayment.objects.create(
                    school=school,
                    student=inv.student,
                    invoice=inv,
                    amount=amount,
                    method=request.POST.get('method', 'CASH'),
                    reference=request.POST.get('reference', ''),
                    recorded_by=request.user,
                )
                inv.amount_paid = float(inv.amount_paid) + amount
                inv.balance = max(0, float(inv.total_amount) - float(inv.amount_paid))
                inv.status = (
                    'PAID' if inv.balance <= 0 else 'PARTIAL' if inv.amount_paid > 0 else 'PENDING'
                )
                inv.save()
                messages.success(request, 'Payment recorded.')
        return redirect('fees:admin')

    return render(
        request,
        'fees/admin.html',
        {'items': items, 'invoices': invoices},
    )


@login_required
def fees_parent(request):
    parent = getattr(request.user, 'parent_profile', None)
    children = parent.children.all() if parent else []
    invoices = FeeInvoice.objects.filter(student__in=children).select_related('student')
    return render(request, 'fees/parent.html', {'invoices': invoices, 'children': children})
