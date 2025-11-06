# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.change_password import ChangePassword  # noqa: E501
from swagger_server.models.token import Token  # noqa: E501
from swagger_server.models.user_register import UserRegister  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV3authController(BaseTestCase):
    """V3authController integration test stubs"""

    def test_post_login(self):
        """Test case for post_login

        
        """
        payload = UserRegister()
        headers = [('X_Fields', 'X_Fields_example')]
        response = self.client.open(
            '/api/v3/auth/login',
            method='POST',
            data=json.dumps(payload),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_register(self):
        """Test case for post_register

        
        """
        payload = UserRegister()
        response = self.client.open(
            '/api/v3/auth/register',
            method='POST',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_reset_password(self):
        """Test case for put_reset_password

        
        """
        payload = ChangePassword()
        response = self.client.open(
            '/api/v3/auth/password',
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
