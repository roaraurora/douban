# -*- coding: utf-8 -*-
# @File  : dto.py
# @Author: deeeeeeeee
# @Date  : 2018/6/30
"""data transfer object"""
from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user operations')  # just like API blueprint
    user_create = api.model(name='user_create', model={
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })
    user_detail = api.model(name='user_detail', model={
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'public_id': fields.String(description='user Identifier'),
        'registered_on': fields.DateTime(description='user registered time'),
        'admin': fields.Boolean(description='is admin'),
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(requried=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
    })


class MovieDto:
    api = Namespace('movie', description='movie relation operation')

    movie = api.model(name='Movie', model={
        'name': fields.String(required=True, description='Movie name'),
        'picture': fields.String(required=True, description='Movie picture'),
        'category': fields.String(required=True, description='Movie name'),
        'url': fields.String(required=True, description='Movie url'),
    })

    pagination = api.model(name='pagination', model={
        'page': fields.Integer(description='Number of this page of results'),
        'pages': fields.Integer(description='Total number of pages of results'),
        'per_page': fields.Integer(description='Number of items per page of result'),
        'total': fields.Integer(description='Total number of result'),
    })
    page_of_movie = api.inherit('page of movie', pagination, {
        'items': fields.List(fields.Nested(movie))
    })
    movie_detail = api.model(name='movie detail', model={
        'name': fields.String(required=True, description='Movie name'),
        'picture': fields.String(required=True, description='Movie picture'),
        'category': fields.String(required=True, description='Movie name'),
        'description': fields.String(required=False, description='Movie description'),
        'cast': fields.String(required=False, description='Movie cast'),
        'rank': fields.Integer(required=True, description='Movie rank'),
        'score': fields.String(required=True, description='Movie score'),
        'url': fields.String(required=True, description='Movie url'),
    })
