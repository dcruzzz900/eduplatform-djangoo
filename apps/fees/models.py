from django.conf import settings
from django.db import models


class FeeItem(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='fee_items')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('school', 'name')]
        ordering = ['name']

    def __str__(self):
        return f'{self.name} (₦{self.amount})'


class FeeInvoice(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PARTIAL = 'PARTIAL', 'Partial'
        PAID = 'PAID', 'Paid'
        CANCELLED = 'CANCELLED', 'Cancelled'

    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='invoices')
    student = models.ForeignKey('academics.Student', on_delete=models.CASCADE, related_name='invoices')
    reference = models.CharField(max_length=40)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('school', 'reference')]
        ordering = ['-created_at']


class FeePayment(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey('academics.Student', on_delete=models.CASCADE, related_name='payments')
    invoice = models.ForeignKey(
        FeeInvoice, null=True, blank=True, on_delete=models.SET_NULL, related_name='payments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, default='CASH')
    reference = models.CharField(max_length=80, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
