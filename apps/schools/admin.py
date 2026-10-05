from django.contrib import admin
from .models import AuditLog, School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_id', 'tenant_id', 'status', 'created_at')
    search_fields = ('name', 'school_id', 'tenant_id')
    readonly_fields = ('school_id', 'tenant_id')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'school', 'actor', 'created_at')
    list_filter = ('action',)
