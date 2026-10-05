def tenant_context(request):
    school = getattr(request, 'school', None)
    return {
        'current_school': school,
        'tenant_id': getattr(school, 'tenant_id', None) if school else None,
    }
