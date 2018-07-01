# -*- coding: utf-8 -*-
# @File  : dto.py
# @Author: deeeeeeeee
# @Date  : 2018/6/30
"""data transfer object"""
from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user operations')  # just like API blueprint
    user = api.model(name='user', model={
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(requried=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
    })
