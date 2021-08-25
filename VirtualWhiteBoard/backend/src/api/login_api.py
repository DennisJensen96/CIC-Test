# Standard library

# VirtualBoard components
from werkzeug.exceptions import Unauthorized
from database.db_interface import Interface, ActionState
from logger.log import get_logger

# Third party library
from flask_restful import Resource, reqparse


class Users(Resource):
    """[summary]
    Endpoint for extracting users.
    """

    def __init__(self) -> None:
        self.__db_interface = Interface()
        self.__logger = get_logger(__file__)

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_name', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('email', required=False)

        args = parser.parse_args()
        self.__logger.debug(f"{args}")
        state: ActionState = self.__db_interface.create_user(
            args['user_name'], args["password"], args["email"])

        if state == ActionState.SUCCESS:
            return {}, 200

        # assuming_user_input_was_wrong
        forbidden = 403
        return {}, forbidden


class Authentication(Resource):
    """[summary]

    Args:
        Resource ([type]): [description]
    """

    def __init__(self) -> None:
        self.__db_interface = Interface()

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_name', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()
        state: ActionState = self.__db_interface.authenticate_user(
            args["user_name"], args["password"])

        if state == ActionState.SUCCESS:
            return {}, 200

        unauthorized_response = 401
        return {}, unauthorized_response


class ResetPassword(Resource):
    """[summary]

    Args:
        Resource ([type]): [description]
    """

    def __init__(self) -> None:
        self.__db_interface = Interface()
