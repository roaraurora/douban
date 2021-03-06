"""
flask_restplus auto jsonify
"""
import uuid
from datetime import datetime
from project.main import db

from project.main.model.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.utcnow()
        )
        save_changes(new_user)

        return generate_token(new_user)
    else:
        # 用户名已存在
        response_object = {
            'status': 'fail',
            'message': 'User already exists.Please Log in.',
        }
        return response_object, 409


def modify_a_user(user, data):
    user.admin = data['admin']
    user.username = data['username']
    db.session.update(user)
    db.session.commit()
    return {
        'status': 'success',
        'message': 'User modify success.',
    }


def delete_a_user(user):
    db.session.delete(user)
    db.session.commit()
    return {
        'status': 'success',
        'message': 'User delete success.',
    }


def search_all_user(search_string):
    if search_string:
        return User.query.filter(User.username.like("%{}%".format(search_string)))
    return get_all_users()


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201  # HTTP code 201:created
    except Exception as e:
        print("user_service.generate_token: {}".format(e))
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
