from django.contrib import admin
from .models import (
    AcademicSession,
    ClassArm,
    Department,
    ParentProfile,
    SchoolClass,
    Student,
    Subject,
    Term,
)

admin.site.register(AcademicSession)
admin.site.register(Term)
admin.site.register(Department)
admin.site.register(SchoolClass)
admin.site.register(ClassArm)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(ParentProfile)
