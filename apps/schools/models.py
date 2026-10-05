import secrets
import string

from django.db import models
from django.utils.text import slugify


def generate_tenant_id():
    alphabet = string.ascii_uppercase + string.digits
    return 'TEN-' + ''.join(secrets.choice(alphabet) for _ in range(6))


def generate_school_id(name: str):
    base = slugify(name).replace('-', '').upper()[:12] or 'SCHOOL'
    suffix = ''.join(secrets.choice(string.digits) for _ in range(3))
    return f'{base}{suffix}'


class School(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACTIVE = 'ACTIVE', 'Active'
        SUSPENDED = 'SUSPENDED', 'Suspended'

    class Level(models.TextChoices):
        NURSERY = 'NURSERY', 'Nursery'
        PRIMARY = 'PRIMARY', 'Primary'
        SECONDARY = 'SECONDARY', 'Secondary'

    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, blank=True)
    school_id = models.CharField(max_length=40, unique=True, editable=False)
    tenant_id = models.CharField(max_length=20, unique=True, editable=False)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Nigeria')
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    levels = models.JSONField(default=list, blank=True)  # ['NURSERY','PRIMARY','SECONDARY']
    motto = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.tenant_id:
            tid = generate_tenant_id()
            while School.objects.filter(tenant_id=tid).exists():
                tid = generate_tenant_id()
            self.tenant_id = tid
        if not self.school_id:
            sid = generate_school_id(self.name)
            while School.objects.filter(school_id=sid).exists():
                sid = generate_school_id(self.name)
            self.school_id = sid
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.school_id})'


class AuditLog(models.Model):
    school = models.ForeignKey(
        School, null=True, blank=True, on_delete=models.SET_NULL, related_name='audit_logs'
    )
    actor = models.ForeignKey(
        'accounts.User', null=True, blank=True, on_delete=models.SET_NULL
    )
    action = models.CharField(max_length=80)
    entity_type = models.CharField(max_length=80, blank=True)
    entity_id = models.CharField(max_length=64, blank=True)
    detail = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
