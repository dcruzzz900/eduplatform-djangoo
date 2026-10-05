from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'school', 'is_super_admin', 'is_staff')
    list_filter = ('role', 'is_super_admin', 'school')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('EduPlatform', {'fields': ('role', 'school', 'phone', 'is_super_admin')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('EduPlatform', {'fields': ('role', 'school', 'is_super_admin')}),
    )
