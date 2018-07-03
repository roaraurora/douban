# -*- coding: utf-8 -*-
# @File  : user.py.py
# @Author: deeeeeeeee
# @Date  : 2018/6/30
from .. import db, flask_bcrypt
import datetime
from project.main.model.blacklist import BlacklistToken
from ..config import key
import jwt


class User(db.Model):
    """User Model"""
    __table__name = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.String(100), unique=True)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    # last_seen = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    # remember_me = db.Column(db.Integer, nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError('password: wrote-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'".format(self.username)

    # def __eq__(self, other):
    #     if self or other:
    #         if self.id == other.id:
    #             return True
    #     return False

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Toekn
        :param user_id:  接受一个用户ID
        :return: string  返回一个完整的 json web token 对象 / 或抛出异常
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),  # 过期时间
                'iat': datetime.datetime.utcnow(),  # 生成时间 issued at time
                'sub': user_id  # subject
            }
            return jwt.encode(
                payload,
                key,  # define in config.py
                algorithm='HS256'  # HMAC sha256
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string user_id
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                # 已加入黑名单
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']  # user_id
        except jwt.ExpiredSignatureError:
            return 'Signature expired.Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token.Please log in again.'
