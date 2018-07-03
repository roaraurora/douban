from flask_restplus import reqparse

user_arguments = reqparse.RequestParser()
user_arguments.add_argument('detail', required=False, location='args')
