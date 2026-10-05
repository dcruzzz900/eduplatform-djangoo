from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from apps.academics.models import SchoolClass, Student, Subject
from apps.schools.models import School

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed Super Admin, demo school, school admin, sample class/subject/student'

    def handle(self, *args, **options):
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create_user(
                username='superadmin',
                email='superadmin@platform.com',
                password='SuperAdmin@123',
                first_name='Platform',
                last_name='SuperAdmin',
                role=User.Role.SUPER_ADMIN,
                is_super_admin=True,
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS('Created superadmin / SuperAdmin@123'))

        school, created = School.objects.get_or_create(
            school_id='GSSGONINGORA',
            defaults={
                'name': 'GSS Goningora',
                'short_name': 'GSSG',
                'tenant_id': 'TEN-DEMO01',
                'city': 'Kaduna',
                'state': 'Kaduna',
                'status': School.Status.ACTIVE,
                'levels': ['SECONDARY'],
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created school {school.name}'))

        if not User.objects.filter(username='schooladmin').exists():
            User.objects.create_user(
                username='schooladmin',
                email='admin@gssgoningora.edu.ng',
                password='SchoolAdmin@123',
                first_name='School',
                last_name='Admin',
                role=User.Role.SCHOOL_ADMIN,
                school=school,
                is_staff=True,
            )
            self.stdout.write(self.style.SUCCESS('Created schooladmin / SchoolAdmin@123'))

        cls, _ = SchoolClass.objects.get_or_create(
            school=school, name='JSS1', defaults={'level': 'SECONDARY', 'order': 1}
        )
        Subject.objects.get_or_create(school=school, name='Mathematics', defaults={'code': 'MTH'})
        Subject.objects.get_or_create(school=school, name='English Language', defaults={'code': 'ENG'})
        Student.objects.get_or_create(
            school=school,
            admission_no='GSS/2026/0001',
            defaults={
                'first_name': 'Amina',
                'last_name': 'Bello',
                'gender': 'FEMALE',
                'school_class': cls,
                'status': 'ACTIVE',
            },
        )
        self.stdout.write(self.style.SUCCESS('Demo data ready.'))
