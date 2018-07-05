from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, search_all_user, modify_a_user, \
    delete_a_user
from ..util.decorators import token_required, admin_token_required
from ..util.parser import user_arguments
from ..service.auth_helper import Auth

api = UserDto.api
_user_create = UserDto.user_create
_user_detail = UserDto.user_detail


@api.route('')
class UserList(Resource):
    @admin_token_required  # warrant decorator need to be top of all decorator
    @api.doc('list_of_registered_users')
    @api.expect(user_arguments, validate=True)
    @api.marshal_list_with(_user_detail, skip_none=True)
    def get(self):
        """list all registered users"""
        args = user_arguments.parse_args(request)
        search_string = args.get('search', None)
        return search_all_user(search_string)

    @api.expect(_user_create, validate=True)
    @api.response(201, 'User successfully created')  # response add api doc
    @api.doc('create a new user')
    def post(self):
        """create a new user"""
        data = request.json
        return save_new_user(data=data)

    # def option(self):
    #     """"""
    #     return 200, {'Access-Control-Allow-Origin': '*'}


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found')
class UserById(Resource):
    @token_required
    @api.doc('get a user')
    @api.marshal_with(_user_create, skip_none=True)  # 将user dto作为序列化的对象
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        print("User by id : {}".format(user))
        if user:
            return user
        else:
            api.abort(404, status='fail', message='User not found')


@api.route('/<public_id>/detail')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found')
class UserDetailById(Resource):
    # @api.expect(user_arguments)
    @token_required
    @api.doc('get a user full detail and required warrant')
    @api.marshal_with(_user_detail)  # 将user dto作为序列化的对象
    @api.response(403, "You have no warrant to this user's detail")
    def get(self, public_id):
        """get a user given its identifier"""
        # args = user_arguments.parse_args(request)
        # detail = args.get('detail', None)  # default none
        # print("args: detail => {}".format(detail))
        user = get_a_user(public_id)
        print(user, type(user))
        if user is None:
            api.abort(404, status='fail', message='User not found')
        current_user_object, status = Auth.get_logged_in_user(request)
        current_user_id = current_user_object.get('data').get('user_id')
        current_user_is_admin = current_user_object.get('data').get('admin')
        if current_user_id == user.id or current_user_is_admin:
            return user
        api.abort(403, status='fail', message="You current have no warrant to this user's detail")

    @admin_token_required
    @api.doc('modify a user full detail and required warrant')
    def put(self, public_id):
        user = get_a_user(public_id)
        data = request.json
        response, status = modify_a_user(data, user)
        return response, status

    @admin_token_required
    def delete(self, public_id):
        user = get_a_user(public_id)
        response, status = delete_a_user(user)
        return response, status
