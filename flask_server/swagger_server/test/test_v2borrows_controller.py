# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.borrow import Borrow  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV2borrowsController(BaseTestCase):
    """V2borrowsController integration test stubs"""

    def test_admin_update_borrow(self):
        """Test case for admin_update_borrow

        Admin update borrow record
        """
        payload = Borrow()
        response = self.client.open(
            '/api/v2/borrows/{borrow_id}'.format(borrow_id=56),
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_borrow_book(self):
        """Test case for borrow_book

        Borrow a book
        """
        query_string = [('book_id', 'book_id_example'),
                        ('user_id', 'user_id_example')]
        response = self.client.open(
            '/api/v2/borrows/',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_borrow(self):
        """Test case for delete_borrow

        Delete a borrow record
        """
        response = self.client.open(
            '/api/v2/borrows/{borrow_id}'.format(borrow_id=56),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_borrows(self):
        """Test case for list_borrows

        List borrows (optionally filtered by user)
        """
        query_string = [('user_id', 'user_id_example')]
        response = self.client.open(
            '/api/v2/borrows/',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_return_borrow(self):
        """Test case for return_borrow

        Return a borrowed copy
        """
        response = self.client.open(
            '/api/v2/borrows/{borrow_id}'.format(borrow_id=56),
            method='PATCH',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
