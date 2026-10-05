from django.contrib import admin
from .models import FeeInvoice, FeeItem, FeePayment

admin.site.register(FeeItem)
admin.site.register(FeeInvoice)
admin.site.register(FeePayment)
