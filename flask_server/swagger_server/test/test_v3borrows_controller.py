# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestV3borrowsController(BaseTestCase):
    """V3borrowsController integration test stubs"""

    def test_borrow_book(self):
        """Test case for borrow_book

        Borrow a book
        """
        query_string = [('book_id', 'book_id_example')]
        response = self.client.open(
            '/api/v3/borrows/',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_borrows(self):
        """Test case for list_borrows

        List borrows (optionally filtered by user)
        """
        response = self.client.open(
            '/api/v3/borrows/',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_return_borrow(self):
        """Test case for return_borrow

        Return a borrowed copy
        """
        response = self.client.open(
            '/api/v3/borrows/',
            method='PATCH',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
