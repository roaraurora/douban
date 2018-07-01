from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user
from ..util.decorators import token_required, admin_token_required

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @token_required
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """list all registered users"""
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created')
    @api.doc('create a new user')
    def post(self):
        """create a new user"""
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)  # 将user dto作为序列化的对象
    # @token_required
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if user:
            return user
        api.abort(404)
