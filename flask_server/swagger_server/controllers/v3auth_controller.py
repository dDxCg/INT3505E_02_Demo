import connexion
import six

from swagger_server.models.change_password import ChangePassword  # noqa: E501
from swagger_server.models.token import Token  # noqa: E501
from swagger_server.models.user_register import UserRegister  # noqa: E501
from swagger_server import util


def post_login(payload, X_Fields=None):  # noqa: E501
    """post_login

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes
    :param X_Fields: An optional fields mask
    :type X_Fields: str

    :rtype: Token
    """
    if connexion.request.is_json:
        payload = UserRegister.from_dict(connexion.request.get_json())  # noqa: E501
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
