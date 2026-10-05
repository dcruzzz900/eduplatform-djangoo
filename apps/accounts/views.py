from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from apps.accounts.models import User
from apps.academics.models import Student
from apps.attendance.models import AttendanceRecord
from apps.fees.models import FeeInvoice
from apps.notices.models import Notice
from apps.results.models import Result
from apps.schools.models import School


class AppLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def dashboard_home(request):
    user = request.user
    if user.is_super_admin or user.role == User.Role.SUPER_ADMIN:
        return redirect('dashboards:super_admin')
    role = user.role
    if role == User.Role.SCHOOL_ADMIN:
        return redirect('dashboards:school_admin')
    if role == User.Role.TEACHER:
        return redirect('dashboards:teacher')
    if role == User.Role.STUDENT:
        return redirect('dashboards:student')
    if role == User.Role.PARENT:
        return redirect('dashboards:parent')
    return redirect('dashboards:school_admin')


@login_required
def super_admin_dashboard(request):
    if not (request.user.is_super_admin or request.user.role == User.Role.SUPER_ADMIN):
        messages.error(request, 'Access denied.')
        return redirect('dashboards:home')
    ctx = {
        'schools_count': School.objects.count(),
        'active_schools': School.objects.filter(status=School.Status.ACTIVE).count(),
        'students_count': Student.objects.count(),
        'users_count': User.objects.count(),
        'schools': School.objects.order_by('-created_at')[:10],
    }
    return render(request, 'dashboards/super_admin.html', ctx)


@login_required
def school_admin_dashboard(request):
    school = request.user.school
    if not school and not request.user.is_super_admin:
        messages.error(request, 'No school linked to your account.')
        return redirect('accounts:login')
    qs_school = school
    notices = Notice.objects.filter(school=qs_school, is_published=True)[:5] if qs_school else []
    ctx = {
        'school': qs_school,
        'students_count': Student.objects.filter(school=qs_school).count() if qs_school else 0,
        'classes_count': qs_school.classes.count() if qs_school else 0,
        'notices': notices,
    }
    return render(request, 'dashboards/school_admin.html', ctx)


@login_required
def teacher_dashboard(request):
    school = request.user.school
    notices = Notice.objects.filter(school=school, is_published=True)[:5] if school else []
    return render(request, 'dashboards/teacher.html', {'notices': notices, 'school': school})


@login_required
def student_dashboard(request):
    school = request.user.school
    student = getattr(request.user, 'student_profile', None)
    results = []
    if student:
        results = Result.objects.filter(
            student=student, status__in=['PUBLISHED', 'LOCKED']
        ).select_related('subject')[:10]
    notices = Notice.objects.filter(school=school, is_published=True)[:5] if school else []
    return render(
        request,
        'dashboards/student.html',
        {'student': student, 'results': results, 'notices': notices},
    )


@login_required
def parent_dashboard(request):
    school = request.user.school
    parent = getattr(request.user, 'parent_profile', None)
    children = parent.children.all() if parent else []
    notices = Notice.objects.filter(school=school, is_published=True)[:5] if school else []
    return render(
        request,
        'dashboards/parent.html',
        {'parent': parent, 'children': children, 'notices': notices},
    )
