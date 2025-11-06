# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.copy import Copy  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV3admincopiesController(BaseTestCase):
    """V3admincopiesController integration test stubs"""

    def test_create_copy(self):
        """Test case for create_copy

        Create a new copy for a book
        """
        payload = Copy()
        query_string = [('book_id', 'book_id_example')]
        response = self.client.open(
            '/api/v3/admin/copies/',
            method='POST',
            data=json.dumps(payload),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_copy(self):
        """Test case for delete_copy

        Delete a copy
        """
        response = self.client.open(
            '/api/v3/admin/copies/{copy_id}'.format(copy_id=56),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_copies(self):
        """Test case for get_copies

        Get all copies for a book
        """
        query_string = [('book_id', 'book_id_example')]
        response = self.client.open(
            '/api/v3/admin/copies/',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_copy(self):
        """Test case for update_copy

        Update a copy
        """
        payload = Copy()
        response = self.client.open(
            '/api/v3/admin/copies/{copy_id}'.format(copy_id=56),
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
