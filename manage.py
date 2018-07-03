# -*- coding: utf-8 -*-
# @File  : manage.py.py
# @Author: deeeeeeeee
# @Date  : 2018/6/29

"""
todo:soon or later i will replace this flask_scripts with click
"""
import os
import unittest
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from project.main import create_app, db
from project import blueprint
import json
from project.main.model import user, blacklist, movie

# todo import and manage.py could detect this and migrate working

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()

# app.response_class = MyResponse

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/test', methods=['GET'])
def test_view():
    t = {
        'a': '3',
    }
    res = json.dumps(t)
    return res


# @app.route('/html')
# def test_view1():
#     return render_template('02-upfile.html')


@manager.command
def run():
    app.run(host='0.0.0.0', debug=True)  # 局域网地址


@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'x-requested-with,Content-Type,Authorization')
    # response.headers.add('Access-Control-Allow-Methods', 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT')
    return response


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=user.User, BlacklistToken=blacklist.BlacklistToken, Movie=movie.Movie,
                read_movie=movie.read_movie)


manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def test():
    """run unit test"""
    tests = unittest.TestLoader().discover('project/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
