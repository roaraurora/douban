from flask_testing import TestCase
from project.main import db
from manage import app


class BaseTestCase(TestCase):
    """Base Test: set up test env"""

    def create_app(self):
        app.config.from_object('project.main.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
