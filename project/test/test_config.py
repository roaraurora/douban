# -*- coding: utf-8 -*-
# @File  : test_config.py.py
# @Author: deeeeeeeee
# @Date  : 2018/6/30
import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from project.main.config import basedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.main.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == "mysql+pymysql://root:root@127.0.0.1:3306/douban?charset=utf8")


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.main.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config[
                'SQLALCHEMY_DATABASE_URI'] == "mysql+pymysql://root:root@127.0.0.1:3306/douban_test?charset=utf8")


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.main.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
