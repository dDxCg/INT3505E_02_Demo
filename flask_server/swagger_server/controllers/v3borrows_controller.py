import connexion
import six

from swagger_server import util


def borrow_book(book_id):  # noqa: E501
    """Borrow a book

     # noqa: E501

    :param book_id: Book ID
    :type book_id: str

    :rtype: None
    """
    return 'do some magic!'


def list_borrows():  # noqa: E501
    """List borrows (optionally filtered by user)

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def return_borrow():  # noqa: E501
    """Return a borrowed copy

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
