# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.book import Book  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV4booksController(BaseTestCase):
    """V4booksController integration test stubs"""

    def test_get_book_list(self):
        """Test case for get_book_list

        
        """
        query_string = [('author', 'author_example'),
                        ('title', 'title_example')]
        response = self.client.open(
            '/api/v4/books/',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
