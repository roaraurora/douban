import unittest
import json
from project.main import db
from project.test.base import BaseTestCase
from project.main.model.blacklist import BlacklistToken


def register_user(self):
    response = self.client.post(
        # 用test client朝对应的view发post请求
        '/user/',
        data=json.dumps(dict(
            email='test@gmail.com',
            username='username',
            password='123456'
        )),
        content_type='application/json'
    )
    return response


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='test@gmail.com',
            password='123456'
        )),
        content_type='application/json'
    )


def test_login(self):
    # 提取出来的测试登录且 期望成功 时的公用部分
    login_response = login_user(self)
    data = json.loads(login_response.data.decode())
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['message'] == 'Successfully logged in.')
    self.assertTrue(data['Authorization'])
    self.assertTrue(login_response.content_type == 'application/json')
    self.assertEqual(login_response.status_code, 200)
    return data


def test_registration(self):
    # 提取出来的测试注册时且 期望成功 的公用部分
    response = register_user(self)
    data = json.loads(response.data.decode())
    self.assertTrue(data['status'] == 'success')
    self.assertTrue(data['message'] == 'Successfully registered.')
    self.assertTrue(data['Authorization'])
    self.assertTrue(response.content_type == 'application/json')
    self.assertEqual(response.status_code, 201)
    return data


class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """Test for user registration"""
        with self.client:
            # 用python上下文管理器在退出时关闭client
            data = test_registration(self)
            print("\ntest_registration response  => {}".format(data))

    def test_registered_with_already_registered_user(self):
        """Test registration with already registered email"""
        register_user(self)
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            print("\ntest_registered_with_already_registered_user response  => {}".format(data))
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists.Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)

    def test_registered_user_login(self):
        """Test for login of registered-user login"""
        with self.client:
            # user registration
            test_registration(self)

            # registered user login
            data = test_login(self)
            print("\ntest_login response  => {}".format(data))

    def test_non_registered_user_login(self):
        """Test for login of non-registered user"""
        with self.client:
            response = login_user(self)
            data = json.loads(response.data.decode())
            print("\ntest_non_registered_user_login response  => {}".format(data))
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'email or password does not match.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_valid_logout(self):
        """Test for logout before token expires"""
        with self.client:
            # user registration
            test_registration(self)

            # registered user login
            data_login = test_login(self)

            # valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + data_login['Authorization']  # json web token
                )
            )
            data = json.loads(response.data.decode())
            print("\ntest_valid_logout response  => {}".format(data))
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_valid_blacklisted_token_logout(self):
        """Test for logout after a valid token gets blacklisted"""
        with self.client:
            # user registration
            data_register = test_registration(self)

            # registered user login
            data_login = test_login(self)

            # blacklist a valid token
            blacklist_token = BlacklistToken(token=data_login['Authorization'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(Authorization='Bearer ' + data_login['Authorization'])
            )
            data = json.loads(response.data.decode())
            print("\ntest_valid_blacklisted_token_logout response  => {}".format(data))
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
