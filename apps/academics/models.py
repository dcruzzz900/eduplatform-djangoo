from django.conf import settings
from django.db import models


class AcademicSession(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='sessions')
    name = models.CharField(max_length=32)  # 2025/2026
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = [('school', 'name')]
        ordering = ['-start_date']

    def __str__(self):
        return self.name


class Term(models.Model):
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='terms')
    name = models.CharField(max_length=40)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f'{self.name} ({self.session.name})'


class Department(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)

    class Meta:
        unique_together = [('school', 'name')]
        ordering = ['name']

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=50)  # JSS1, Primary 3
    level = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)
    session = models.ForeignKey(
        AcademicSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='classes'
    )

    class Meta:
        verbose_name_plural = 'classes'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class ClassArm(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='arms')
    name = models.CharField(max_length=20)  # A, B, Gold

    class Meta:
        unique_together = [('school_class', 'name')]
        ordering = ['name']

    def __str__(self):
        return f'{self.school_class.name} {self.name}'


class Subject(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    department = models.ForeignKey(
        Department, null=True, blank=True, on_delete=models.SET_NULL, related_name='subjects'
    )

    class Meta:
        unique_together = [('school', 'name')]
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        GRADUATED = 'GRADUATED', 'Graduated'
        TRANSFERRED = 'TRANSFERRED', 'Transferred'

    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
        OTHER = 'OTHER', 'Other'

    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='students')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='student_profile'
    )
    admission_no = models.CharField(max_length=40)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    other_names = models.CharField(max_length=80, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    school_class = models.ForeignKey(
        SchoolClass, null=True, blank=True, on_delete=models.SET_NULL, related_name='students'
    )
    arm = models.ForeignKey(ClassArm, null=True, blank=True, on_delete=models.SET_NULL, related_name='students')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('school', 'admission_no')]
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.admission_no})'

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name}'.strip()


class ParentProfile(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='parents')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profile'
    )
    relationship = models.CharField(max_length=40, blank=True)
    children = models.ManyToManyField(Student, blank=True, related_name='parents')

    def __str__(self):
        return str(self.user)
