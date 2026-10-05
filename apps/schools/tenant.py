"""Helpers to enforce tenant-scoped querysets."""


def school_filter(user):
    """Return Q-kwargs for filtering by the user's school."""
    if not user or not user.is_authenticated:
        return {'pk__in': []}
    if getattr(user, 'is_super_admin', False):
        return {}
    if user.school_id:
        return {'school_id': user.school_id}
    return {'pk__in': []}


def require_school(user):
    if getattr(user, 'is_super_admin', False):
        return None
    return getattr(user, 'school', None)
