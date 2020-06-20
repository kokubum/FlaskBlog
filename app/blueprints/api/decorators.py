from app.models import Permission
from functools import wraps
from flask import g
from .errors import forbidden

def permission_required(perm):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args,**kwargs):
            if not g.current_user.can(perm):
                return forbidden('Insufficient permissions')
            return f(*args,**kwargs)
        return decorated_func
    return decorator