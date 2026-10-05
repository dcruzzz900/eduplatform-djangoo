from django.conf import settings
from django.db import models
from django.utils import timezone


class Notice(models.Model):
    class Audience(models.TextChoices):
        ALL = 'ALL', 'Everyone'
        STAFF = 'STAFF', 'Staff'
        TEACHERS = 'TEACHERS', 'Teachers'
        STUDENTS = 'STUDENTS', 'Students'
        PARENTS = 'PARENTS', 'Parents'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        NORMAL = 'NORMAL', 'Normal'
        HIGH = 'HIGH', 'High'
        URGENT = 'URGENT', 'Urgent'

    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='notices')
    title = models.CharField(max_length=200)
    body = models.TextField()
    audience = models.CharField(max_length=12, choices=Audience.choices, default=Audience.ALL)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.NORMAL)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
