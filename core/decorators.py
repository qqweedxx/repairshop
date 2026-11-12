from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def role_required(*roles):
    """
    Декоратор: пускает только пользователей с указанной ролью.
    Использование: @role_required('client') или @role_required('master', 'admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied('У вас нет доступа к этой странице.')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator