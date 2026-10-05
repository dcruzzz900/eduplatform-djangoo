from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.academics.models import ClassArm, SchoolClass, Student, Subject


def _school_or_deny(request):
    school = request.user.school
    if not school:
        messages.error(request, 'No school context.')
        return None
    return school


@login_required
def class_list(request):
    school = _school_or_deny(request)
    if not school:
        return redirect('dashboards:home')
    classes = SchoolClass.objects.filter(school=school).prefetch_related('arms')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            SchoolClass.objects.create(
                school=school,
                name=name,
                level=request.POST.get('level', ''),
                order=int(request.POST.get('order') or 0),
            )
            messages.success(request, 'Class created.')
            return redirect('academics:classes')
    return render(request, 'academics/classes.html', {'classes': classes})


@login_required
def subject_list(request):
    school = _school_or_deny(request)
    if not school:
        return redirect('dashboards:home')
    subjects = Subject.objects.filter(school=school)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Subject.objects.create(
                school=school,
                name=name,
                code=request.POST.get('code', '').strip(),
            )
            messages.success(request, 'Subject created.')
            return redirect('academics:subjects')
    return render(request, 'academics/subjects.html', {'subjects': subjects})


@login_required
def student_list(request):
    school = _school_or_deny(request)
    if not school:
        return redirect('dashboards:home')
    students = Student.objects.filter(school=school).select_related('school_class', 'arm')
    classes = SchoolClass.objects.filter(school=school)
    return render(
        request,
        'academics/students.html',
        {'students': students, 'classes': classes},
    )


@login_required
def student_enrol(request):
    school = _school_or_deny(request)
    if not school:
        return redirect('dashboards:home')
    classes = SchoolClass.objects.filter(school=school).prefetch_related('arms')
    if request.method == 'POST':
        first = request.POST.get('first_name', '').strip()
        last = request.POST.get('last_name', '').strip()
        adm = request.POST.get('admission_no', '').strip()
        if not first or not last:
            messages.error(request, 'Name is required.')
        else:
            if not adm:
                adm = f'{school.school_id[:6]}/{timezone.now().year}/{Student.objects.filter(school=school).count() + 1:04d}'
            Student.objects.create(
                school=school,
                first_name=first,
                last_name=last,
                other_names=request.POST.get('other_names', '').strip(),
                admission_no=adm,
                gender=request.POST.get('gender', ''),
                school_class_id=request.POST.get('class_id') or None,
                arm_id=request.POST.get('arm_id') or None,
            )
            messages.success(request, f'Student enrolled ({adm}).')
            return redirect('academics:students')
    return render(request, 'academics/student_enrol.html', {'classes': classes})
