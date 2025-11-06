# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.copy import Copy  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV2copiesController(BaseTestCase):
    """V2copiesController integration test stubs"""

    def test_create_copy(self):
        """Test case for create_copy

        Create a new copy for a book
        """
        payload = Copy()
        response = self.client.open(
            '/api/v2/copies/book/{book_id}'.format(book_id=56),
            method='POST',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_copy(self):
        """Test case for delete_copy

        Delete a copy
        """
        response = self.client.open(
            '/api/v2/copies/{copy_id}'.format(copy_id=56),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_copies(self):
        """Test case for get_copies

        Get all copies for a book
        """
        response = self.client.open(
            '/api/v2/copies/book/{book_id}'.format(book_id=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_copy(self):
        """Test case for update_copy

        Update a copy
        """
        payload = Copy()
        response = self.client.open(
            '/api/v2/copies/{copy_id}'.format(copy_id=56),
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
