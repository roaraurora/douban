from flask import request
from flask_restplus import Resource

from project.main.service.auth_helper import Auth
from ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
    User login Resource
    """

    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json  # {data:{email:value,email:value}}
        return Auth.login_user(data=post_data)  # response_object, status code(200/401/500)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @api.doc('logout a user')
    def post(self):
        # get auth token
        # todo:我有一个大胆的想法,返回的response对象中的token被客户端解析后识别出jwt标准就把该死的token加到了首部字段Authorization里面
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)  # response_object, status code(200/401/500)
