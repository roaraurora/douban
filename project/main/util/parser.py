from flask_restplus import reqparse

user_arguments = reqparse.RequestParser()
user_arguments.add_argument('detail', required=False, location='args')

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 16, 20, 30, 40, 50],
                                  default=16, help='Results per page {error_msg}')
# pagination_arguments.add_argument('query', type=str, required=False, default=None, help='Page query string')
