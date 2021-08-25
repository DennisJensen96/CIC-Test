"""[summary]
This module adds the ability to interface with an SQLite3 database
"""

# Standard library
import os
from enum import Enum
import sqlite3
import hashlib

# VirtualWhiteBoard Project
from logger.log import get_logger


class ActionState(Enum):
    """[summary]
    An enum state drive for database operations.
    """
    SUCCESS = 0
    FAILED = 1
    ABORTED = 2
    TIMED_OUT = 3


class DatabaseConnection:

    def __init__(self) -> None:
        """[summary]
        Base database connection method
        """
        self.__logger = get_logger("db_connection")
        base_path = "./data"
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        self._db__connection = sqlite3.connect(
            f'{base_path}/data.db')
        self._cursor = self._db__connection.cursor()

        self.__logger.info("Connection established")


class Interface(DatabaseConnection):
    """[summary]
    Class object to enable storage of odds to an SQLite3 database
    """

    def __init__(self,) -> None:
        super().__init__()
        self.__logger = get_logger("db_interface")

        state: ActionState = self.__create_table("virtual_white_board")

        assert state == ActionState.SUCCESS, "Was not able to create table for client database"

    def __del__(self) -> None:
        self._db__connection.close()

    def __create_table(self, website_name: str) -> ActionState:
        sql_query_odds_table = f''' CREATE TABLE IF NOT EXISTS {website_name} (
                                        user_name TEXT PRIMARY KEY NOT NULL,
                                        password TEXT KEY NOT NULL,
                                        email TEXT,
                                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                                    ); '''

        try:
            self._cursor.execute(sql_query_odds_table)
            return ActionState.SUCCESS
        except Exception as error:
            self.__logger.error(f'Unable to create table error: {error}')
            return ActionState.FAILED

    def __hash_password(password: str):
        h: hashlib._Hash = hashlib.sha256()
        h.update(password)
        return str(h.digest())

    def create_user(self, user_name: str, password: str, email: str = ""):
        hashed_password: str = self.__hash_password(password)
