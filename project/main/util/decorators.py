from functools import wraps
from flask import request
from project.main.service.auth_helper import Auth


def \
        token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        print("decorator token_required data: {}".format(data))
        token = data.get('data')
        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response, 401

        return f(*args, **kwargs)

    return decorated


def self_or_admin_required(public_id: str):
    """only self or admin could visit"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data, status = Auth.get_logged_in_user(request)
            token = data.get('data')

            if not token:
                return data, status

            admin = token.get('admin')
            if admin or public_id == data.get('public_id'):
                return f(*args, **kwargs)
            response = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response, 401

        return wrapper

    return decorator
