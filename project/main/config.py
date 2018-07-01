# -*- coding: utf-8 -*-
# @File  : config.py.py
# @Author: deeeeeeeee
# @Date  : 2018/6/29
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_project_secret_key')
    DEBUG = False

    @staticmethod
    def get_db_uri(DATABASE: str) -> str:
        DIALECT = 'mysql'
        DRIVER = 'pymysql'
        USERNAME = 'root'
        PASSWORD = 'root'
        HOST = '127.0.0.1'
        PORT = '3306'
        SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD,
                                                                               HOST, PORT, DATABASE)
        return SQLALCHEMY_DATABASE_URI


class DevelopmentConfig(Config):
    DEBUG = True

    DATABASE = 'douban'
    SQLALCHEMY_DATABASE_URI = Config.get_db_uri(DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def print_uri():
        print("URI： {}".format(DevelopmentConfig.SQLALCHEMY_DATABASE_URI))


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE = 'douban_test'
    SQLALCHEMY_DATABASE_URI = Config.get_db_uri(DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI when needed


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY

if __name__ == '__main__':
    DevelopmentConfig.print_uri()