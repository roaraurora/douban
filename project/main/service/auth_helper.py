from project.main.model.user import User
from ..service.blacklist_service import save_token


class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token(user.id)  # return a jwt or raise exception
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                # user don't exist or password incorrect
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401  # Http status 401:Unauthorized
        except Exception as e:
            print("auth_helper.Auth.login_user: {}".format(e))
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1] # Bearer xxx.xxx.xxx
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)  # user_id or error msg
            if not isinstance(resp, str):
                # mark the token as blacklisted to disabled it
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401

        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        data = new_request.headers.get('Authorization')
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            print(auth_token)
            resp = User.decode_auth_token(auth_token)  # user_id
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200  # 返回user对象
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
