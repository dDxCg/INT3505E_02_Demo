# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.book import Book  # noqa: E501
from swagger_server.models.book_response import BookResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestV7booksController(BaseTestCase):
    """V7booksController integration test stubs"""

    def test_delete_book(self):
        """Test case for delete_book

        Delete a book
        """
        response = self.client.open(
            '/api/v7/books/{id}'.format(id='id_example'),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_book(self):
        """Test case for get_book

        Get a single book by ID
        """
        headers = [('X_Fields', 'X_Fields_example')]
        response = self.client.open(
            '/api/v7/books/{id}'.format(id='id_example'),
            method='GET',
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_book_list(self):
        """Test case for get_book_list

        Get all books or search by query parameters
        """
        query_string = [('title', 'title_example'),
                        ('author', 'author_example'),
                        ('year', 'year_example'),
                        ('genre', 'genre_example')]
        headers = [('X_Fields', 'X_Fields_example')]
        response = self.client.open(
            '/api/v7/books/',
            method='GET',
            headers=headers,
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_book_list(self):
        """Test case for post_book_list

        Add a new book
        """
        payload = Book()
        response = self.client.open(
            '/api/v7/books/',
            method='POST',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_book(self):
        """Test case for put_book

        Update a book
        """
        payload = Book()
        response = self.client.open(
            '/api/v7/books/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
