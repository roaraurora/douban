from functools import wraps
from flask import request

from project.main.service.auth_helper import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        print(data)
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
            response_pbject = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_pbject, 401

        return f(*args, **kwargs)

    return decorated
