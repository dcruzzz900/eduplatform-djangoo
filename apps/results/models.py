from django.conf import settings
from django.db import models


def compute_grade(total):
    if total is None:
        return None
    if total >= 75:
        return 'A'
    if total >= 65:
        return 'B'
    if total >= 55:
        return 'C'
    if total >= 45:
        return 'D'
    if total >= 40:
        return 'E'
    return 'F'


REMARKS = {'A': 'Excellent', 'B': 'Very Good', 'C': 'Good', 'D': 'Fair', 'E': 'Pass', 'F': 'Fail'}


class Result(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        APPROVED = 'APPROVED', 'Approved'
        PUBLISHED = 'PUBLISHED', 'Published'
        LOCKED = 'LOCKED', 'Locked'

    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('academics.Student', on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='results')
    session = models.ForeignKey(
        'academics.AcademicSession', null=True, blank=True, on_delete=models.SET_NULL
    )
    term = models.ForeignKey('academics.Term', null=True, blank=True, on_delete=models.SET_NULL)
    ca_score = models.FloatField(null=True, blank=True)
    exam_score = models.FloatField(null=True, blank=True)
    total_score = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=2, blank=True)
    remark = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    entered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('school', 'student', 'subject', 'session', 'term')]

    def recalculate(self):
        ca = self.ca_score or 0
        exam = self.exam_score or 0
        if self.ca_score is None and self.exam_score is None:
            self.total_score = None
            self.grade = ''
            self.remark = ''
        else:
            self.total_score = round(ca + exam, 2)
            self.grade = compute_grade(self.total_score) or ''
            self.remark = REMARKS.get(self.grade, '')

    def save(self, *args, **kwargs):
        self.recalculate()
        super().save(*args, **kwargs)
