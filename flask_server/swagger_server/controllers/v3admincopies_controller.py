import connexion
import six

from swagger_server.models.copy import Copy  # noqa: E501
from swagger_server import util


def create_copy(payload, book_id=None):  # noqa: E501
    """Create a new copy for a book

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes
    :param book_id: The book ID
    :type book_id: str

    :rtype: None
    """
    if connexion.request.is_json:
        payload = Copy.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_copy(copy_id):  # noqa: E501
    """Delete a copy

     # noqa: E501

    :param copy_id: The copy ID
    :type copy_id: int

    :rtype: None
    """
    return 'do some magic!'


def get_copies(book_id=None):  # noqa: E501
    """Get all copies for a book

     # noqa: E501

    :param book_id: The book ID
    :type book_id: str

    :rtype: None
    """
    return 'do some magic!'


def update_copy(copy_id, payload):  # noqa: E501
    """Update a copy

     # noqa: E501

    :param copy_id: The copy ID
    :type copy_id: int
    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = Copy.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
