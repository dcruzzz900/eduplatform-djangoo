from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.academics.models import SchoolClass, Student
from apps.attendance.models import AttendanceRecord


@login_required
def mark_attendance(request):
    school = request.user.school
    if not school:
        messages.error(request, 'No school context.')
        return redirect('dashboards:home')

    classes = SchoolClass.objects.filter(school=school)
    class_id = request.GET.get('class_id') or request.POST.get('class_id')
    day = request.GET.get('date') or request.POST.get('date') or str(date.today())

    students = []
    existing = {}
    if class_id:
        students = Student.objects.filter(
            school=school, school_class_id=class_id, status='ACTIVE'
        )
        for r in AttendanceRecord.objects.filter(
            school=school, date=day, student__in=students
        ):
            existing[r.student_id] = r

    if request.method == 'POST' and class_id:
        for st in students:
            status = request.POST.get(f'status_{st.id}', 'PRESENT')
            AttendanceRecord.objects.update_or_create(
                school=school,
                student=st,
                date=day,
                defaults={
                    'status': status,
                    'school_class_id': class_id,
                    'marked_by': request.user,
                },
            )
        messages.success(request, 'Attendance saved.')
        return redirect(f'{request.path}?class_id={class_id}&date={day}')

    return render(
        request,
        'attendance/mark.html',
        {
            'classes': classes,
            'students': students,
            'existing': existing,
            'class_id': class_id or '',
            'date': day,
            'statuses': AttendanceRecord.Status.choices,
        },
    )


@login_required
def my_attendance(request):
    student = getattr(request.user, 'student_profile', None)
    records = []
    if student:
        records = AttendanceRecord.objects.filter(student=student)[:60]
    return render(request, 'attendance/my.html', {'records': records, 'student': student})
