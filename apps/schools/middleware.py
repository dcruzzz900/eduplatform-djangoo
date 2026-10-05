from django.utils.functional import SimpleLazyObject


def get_current_school(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated and getattr(user, 'school_id', None):
        return user.school
    return None


class TenantMiddleware:
    """Attach request.school from the authenticated user (never from client-supplied IDs)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.school = SimpleLazyObject(lambda: get_current_school(request))
        return self.get_response(request)
