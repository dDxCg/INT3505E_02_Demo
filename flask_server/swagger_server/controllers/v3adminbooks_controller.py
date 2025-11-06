import connexion
import six

from swagger_server.models.book import Book  # noqa: E501
from swagger_server import util


def create_book(payload):  # noqa: E501
    """Create a new book

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_book(book_id):  # noqa: E501
    """Delete a book

     # noqa: E501

    :param book_id: The book identifier
    :type book_id: int

    :rtype: None
    """
    return 'do some magic!'


def search_books_admin(author=None, title=None, id=None):  # noqa: E501
    """Search books (admin)

     # noqa: E501

    :param author: Filter by author
    :type author: str
    :param title: Filter by title
    :type title: str
    :param id: Filter by book ID
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def update_book(book_id, payload):  # noqa: E501
    """Update a book

     # noqa: E501

    :param book_id: The book identifier
    :type book_id: int
    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
