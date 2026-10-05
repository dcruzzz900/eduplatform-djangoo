from django.conf import settings
from django.db import models


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        LATE = 'LATE', 'Late'
        EXCUSED = 'EXCUSED', 'Excused'

    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='attendance')
    student = models.ForeignKey('academics.Student', on_delete=models.CASCADE, related_name='attendance')
    school_class = models.ForeignKey(
        'academics.SchoolClass', null=True, blank=True, on_delete=models.SET_NULL
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    remarks = models.CharField(max_length=255, blank=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # Offline-friendly client id
    client_id = models.CharField(max_length=64, blank=True)

    class Meta:
        unique_together = [('school', 'student', 'date')]
        ordering = ['-date']
