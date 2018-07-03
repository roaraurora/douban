# -*- coding: utf-8 -*-
# @File  : __init__.py.py
# @Author: deeeeeeeee
# @Date  : 2018/6/29
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    CORS(app, resources={r'/*': {"origins": "*"}}, supports_credentials=True)

    return app
