import connexion
import six

from swagger_server.models.borrow import Borrow  # noqa: E501
from swagger_server import util


def admin_update_borrow(borrow_id, payload):  # noqa: E501
    """Admin update borrow record

     # noqa: E501

    :param borrow_id: Borrow record ID
    :type borrow_id: int
    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = Borrow.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_borrow(borrow_id):  # noqa: E501
    """Delete a borrow record

     # noqa: E501

    :param borrow_id: Borrow record ID
    :type borrow_id: int

    :rtype: None
    """
    return 'do some magic!'


def return_borrow(borrow_id):  # noqa: E501
    """Return a borrowed copy

     # noqa: E501

    :param borrow_id: Borrow record ID
    :type borrow_id: int

    :rtype: None
    """
    return 'do some magic!'
