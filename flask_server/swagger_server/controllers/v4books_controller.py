import connexion
import six

from swagger_server.models.book import Book  # noqa: E501
from swagger_server import util


def get_book_list(author=None, title=None):  # noqa: E501
    """get_book_list

     # noqa: E501

    :param author: Filter by author
    :type author: str
    :param title: Filter by title
    :type title: str

    :rtype: Book
    """
    return 'do some magic!'
