from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import User
from apps.schools.models import AuditLog, School


@login_required
def school_list(request):
    if not (request.user.is_super_admin or request.user.role == User.Role.SUPER_ADMIN):
        messages.error(request, 'Access denied.')
        return redirect('dashboards:home')
    schools = School.objects.all()
    return render(request, 'schools/list.html', {'schools': schools})


@login_required
def school_create(request):
    if not (request.user.is_super_admin or request.user.role == User.Role.SUPER_ADMIN):
        messages.error(request, 'Access denied.')
        return redirect('dashboards:home')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'School name is required.')
        else:
            school = School.objects.create(
                name=name,
                short_name=request.POST.get('short_name', '').strip(),
                address=request.POST.get('address', '').strip(),
                city=request.POST.get('city', '').strip(),
                state=request.POST.get('state', '').strip(),
                phone=request.POST.get('phone', '').strip(),
                email=request.POST.get('email', '').strip(),
                status=School.Status.ACTIVE,
                levels=request.POST.getlist('levels'),
            )
            # Create default school admin
            email = request.POST.get('admin_email', '').strip()
            password = request.POST.get('admin_password', '').strip()
            if email and password:
                User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=request.POST.get('admin_first_name', 'School'),
                    last_name=request.POST.get('admin_last_name', 'Admin'),
                    role=User.Role.SCHOOL_ADMIN,
                    school=school,
                )
            AuditLog.objects.create(
                school=school,
                actor=request.user,
                action='SCHOOL_CREATED',
                entity_type='School',
                entity_id=str(school.pk),
                detail={'school_id': school.school_id, 'tenant_id': school.tenant_id},
            )
            messages.success(
                request,
                f'School created. School ID: {school.school_id} · Tenant: {school.tenant_id}',
            )
            return redirect('schools:list')
    return render(request, 'schools/create.html')


@login_required
def school_detail(request, pk):
    if not (request.user.is_super_admin or request.user.role == User.Role.SUPER_ADMIN):
        messages.error(request, 'Access denied.')
        return redirect('dashboards:home')
    school = get_object_or_404(School, pk=pk)
    return render(request, 'schools/detail.html', {'school': school})
