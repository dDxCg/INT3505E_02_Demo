import connexion
import six

from swagger_server.models.change_password import ChangePassword  # noqa: E501
from swagger_server.models.user_register import UserRegister  # noqa: E501
from swagger_server import util


def post_login(payload):  # noqa: E501
    """post_login

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = UserRegister.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_logout():  # noqa: E501
    """post_logout

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def post_refresh():  # noqa: E501
    """post_refresh

    Rotate refresh token and issue a new access token # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def post_register(payload):  # noqa: E501
    """post_register

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = UserRegister.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def put_reset_password(payload):  # noqa: E501
    """put_reset_password

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payload = ChangePassword.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
