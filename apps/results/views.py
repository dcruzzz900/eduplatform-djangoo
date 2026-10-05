from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.academics.models import SchoolClass, Student, Subject
from apps.results.models import Result


@login_required
def results_entry(request):
    school = request.user.school
    if not school:
        return redirect('dashboards:home')
    classes = SchoolClass.objects.filter(school=school)
    subjects = Subject.objects.filter(school=school)
    class_id = request.GET.get('class_id') or request.POST.get('class_id')
    subject_id = request.GET.get('subject_id') or request.POST.get('subject_id')

    students = []
    rows = {}
    if class_id and subject_id:
        students = Student.objects.filter(school=school, school_class_id=class_id, status='ACTIVE')
        for r in Result.objects.filter(school=school, subject_id=subject_id, student__in=students):
            rows[r.student_id] = r

    if request.method == 'POST' and class_id and subject_id:
        action = request.POST.get('action', 'draft')
        status = 'SUBMITTED' if action == 'submit' else 'DRAFT'
        for st in students:
            ca = request.POST.get(f'ca_{st.id}')
            exam = request.POST.get(f'exam_{st.id}')
            ca_v = float(ca) if ca not in (None, '') else None
            ex_v = float(exam) if exam not in (None, '') else None
            obj, _ = Result.objects.get_or_create(
                school=school,
                student=st,
                subject_id=subject_id,
                session=None,
                term=None,
                defaults={'status': status, 'entered_by': request.user},
            )
            if obj.status in ('APPROVED', 'PUBLISHED', 'LOCKED'):
                continue
            obj.ca_score = ca_v
            obj.exam_score = ex_v
            obj.status = status
            obj.entered_by = request.user
            obj.save()
        messages.success(request, 'Results saved.')
        return redirect(f'{request.path}?class_id={class_id}&subject_id={subject_id}')

    return render(
        request,
        'results/entry.html',
        {
            'classes': classes,
            'subjects': subjects,
            'students': students,
            'rows': rows,
            'class_id': class_id or '',
            'subject_id': subject_id or '',
        },
    )


@login_required
def results_manage(request):
    school = request.user.school
    if not school:
        return redirect('dashboards:home')
    class_id = request.GET.get('class_id') or request.POST.get('class_id')
    subject_id = request.GET.get('subject_id') or request.POST.get('subject_id')
    classes = SchoolClass.objects.filter(school=school)
    subjects = Subject.objects.filter(school=school)

    if request.method == 'POST' and class_id and subject_id:
        action = request.POST.get('action')
        student_ids = list(
            Student.objects.filter(school=school, school_class_id=class_id).values_list('id', flat=True)
        )
        qs = Result.objects.filter(school=school, subject_id=subject_id, student_id__in=student_ids)
        if action == 'approve':
            n = qs.filter(status='SUBMITTED').update(status='APPROVED')
            messages.success(request, f'Approved {n} result(s).')
        elif action == 'publish':
            n = qs.filter(status='APPROVED').update(
                status='PUBLISHED', published_at=timezone.now()
            )
            messages.success(request, f'Published {n} result(s).')
        return redirect(f'{request.path}?class_id={class_id}&subject_id={subject_id}')

    results = []
    if class_id and subject_id:
        results = Result.objects.filter(
            school=school,
            subject_id=subject_id,
            student__school_class_id=class_id,
        ).select_related('student')

    return render(
        request,
        'results/manage.html',
        {
            'classes': classes,
            'subjects': subjects,
            'results': results,
            'class_id': class_id or '',
            'subject_id': subject_id or '',
        },
    )


@login_required
def my_results(request):
    student = getattr(request.user, 'student_profile', None)
    results = []
    if student:
        results = Result.objects.filter(
            student=student, status__in=['PUBLISHED', 'LOCKED']
        ).select_related('subject')
    return render(request, 'results/my.html', {'results': results, 'student': student})


@login_required
def report_card(request, student_id):
    school = request.user.school
    student = get_object_or_404(Student, pk=student_id, school=school)
    # Parents may only see linked children
    if request.user.role == 'PARENT':
        parent = getattr(request.user, 'parent_profile', None)
        if not parent or not parent.children.filter(pk=student.pk).exists():
            messages.error(request, 'Access denied.')
            return redirect('dashboards:parent')
    results = Result.objects.filter(
        student=student, status__in=['PUBLISHED', 'LOCKED']
    ).select_related('subject')
    avg = None
    totals = [r.total_score for r in results if r.total_score is not None]
    if totals:
        avg = round(sum(totals) / len(totals), 1)
    return render(
        request,
        'results/report_card.html',
        {'student': student, 'results': results, 'average': avg, 'school': school},
    )
