from django.http import JsonResponse
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                role = request.user.user_role.role
            except:
                role = "VIEWER"

            if role not in allowed_roles:
                return JsonResponse({
                    "status": "error",
                    "message": "Not Authorized"
                }, status=403)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
