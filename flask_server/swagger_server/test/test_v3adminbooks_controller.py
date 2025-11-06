# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.book import Book  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV3adminbooksController(BaseTestCase):
    """V3adminbooksController integration test stubs"""

    def test_create_book(self):
        """Test case for create_book

        Create a new book
        """
        payload = Book()
        response = self.client.open(
            '/api/v3/admin/books/',
            method='POST',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_book(self):
        """Test case for delete_book

        Delete a book
        """
        response = self.client.open(
            '/api/v3/admin/books/{book_id}'.format(book_id=56),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_books_admin(self):
        """Test case for search_books_admin

        Search books (admin)
        """
        query_string = [('author', 'author_example'),
                        ('title', 'title_example'),
                        ('id', 'id_example')]
        response = self.client.open(
            '/api/v3/admin/books/',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_book(self):
        """Test case for update_book

        Update a book
        """
        payload = Book()
        response = self.client.open(
            '/api/v3/admin/books/{book_id}'.format(book_id=56),
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
