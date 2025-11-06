# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.borrow import Borrow  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV3adminborrowsController(BaseTestCase):
    """V3adminborrowsController integration test stubs"""

    def test_admin_update_borrow(self):
        """Test case for admin_update_borrow

        Admin update borrow record
        """
        payload = Borrow()
        response = self.client.open(
            '/api/v3/admin/borrows/{borrow_id}'.format(borrow_id=56),
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_borrow(self):
        """Test case for delete_borrow

        Delete a borrow record
        """
        response = self.client.open(
            '/api/v3/admin/borrows/{borrow_id}'.format(borrow_id=56),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_return_borrow(self):
        """Test case for return_borrow

        Return a borrowed copy
        """
        response = self.client.open(
            '/api/v3/admin/borrows/{borrow_id}'.format(borrow_id=56),
            method='PATCH',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
