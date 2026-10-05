from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user; tenant isolation via school FK (null for Super Admin)."""

    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
        SCHOOL_ADMIN = 'SCHOOL_ADMIN', 'School Admin'
        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'
        PARENT = 'PARENT', 'Parent'
        STAFF = 'STAFF', 'Staff'

    school = models.ForeignKey(
        'schools.School',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='users',
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STAFF)
    phone = models.CharField(max_length=30, blank=True)
    is_super_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.role})'

    @property
    def tenant_id(self):
        return self.school.tenant_id if self.school_id else None
