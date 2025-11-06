import connexion
import six

from swagger_server.models.book import Book  # noqa: E501
from swagger_server.models.book_response import BookResponse  # noqa: E501
from swagger_server import util


def delete_book(id):  # noqa: E501
    """Delete a book

     # noqa: E501

    :param id: Book ID
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def get_book(id, X_Fields=None):  # noqa: E501
    """Get a single book by ID

     # noqa: E501

    :param id: Book ID
    :type id: str
    :param X_Fields: An optional fields mask
    :type X_Fields: str

    :rtype: BookResponse
    """
    return 'do some magic!'


def get_book_list(title=None, author=None, year=None, genre=None, X_Fields=None):  # noqa: E501
    """Get all books or search by query parameters

     # noqa: E501

    :param title: Search by book title
    :type title: str
    :param author: Search by author name
    :type author: str
    :param year: Filter by publication year
    :type year: str
    :param genre: Filter by genre
    :type genre: str
    :param X_Fields: An optional fields mask
    :type X_Fields: str

    :rtype: List[BookResponse]
    """
    return 'do some magic!'


def post_book_list(payload):  # noqa: E501
    """Add a new book

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def put_book(id, payload):  # noqa: E501
    """Update a book

     # noqa: E501

    :param id: Book ID
    :type id: str
    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
