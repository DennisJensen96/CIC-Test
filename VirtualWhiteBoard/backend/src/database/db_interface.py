"""[summary]
This module adds the ability to interface with an SQLite3 database
"""

# Standard library
from logging import Logger
import os
from enum import Enum
import sqlite3
import hashlib

from pandas.io import sql

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
        self.__logger: Logger = get_logger("db_interface")
        self.user_table: str = "users"
        state: ActionState = self.__create_user_table()

        assert state == ActionState.SUCCESS, "Was not able to create table for client database"

    def __del__(self) -> None:
        self._db__connection.close()

    def __create_user_table(self) -> ActionState:
        sql_query_odds_table = f''' CREATE TABLE IF NOT EXISTS {self.user_table} (
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

    def __hash_password(self, password: str) -> str:
        h: hashlib._Hash = hashlib.sha256()
        h.update(password.encode('utf-8'))
        return str(h.hexdigest())

    def create_user(self, user_name: str, password: str, email: str = None) -> ActionState:
        hashed_password: str = self.__hash_password(password)
        sql_query = f"INSERT INTO {self.user_table} (user_name, password, email) VALUES(?, ?, ?)"

        try:
            self._cursor.execute(
                sql_query, (user_name, hashed_password, email))
        except sqlite3.IntegrityError:
            self.__logger.error("User with that username exists")
            return ActionState.FAILED

        self._db__connection.commit()

        return ActionState.SUCCESS

    def authenticate_user(self, user_name, password) -> ActionState:
        sql_query = f"SELECT user_name, password FROM {self.user_table} WHERE user_name='{user_name}'"
        self._cursor.execute(sql_query)
        data = self._cursor.fetchall()

        if len(data) != 1:
            self.__logger.debug("User was not created")
            return ActionState.FAILED

        password_hash_db = data[0][1]
        current_password_hash = self.__hash_password(password)

        return ActionState.SUCCESS if password_hash_db == current_password_hash else ActionState.FAILED

    def reset_passsword(self, user_name: str, password: str, new_password: str):
        state: ActionState = self.authenticate_user(
            user_name, password)

        if ActionState.FAILED == state:
            self.__logger.debug("Authentication failed on reset password")
            return state
        hashed_new_pass: str = self.__hash_password(
            new_password)

        sql_query = f"UPDATE {self.user_table} SET password='{hashed_new_pass}' WHERE user_name='{user_name}'"
        self._cursor.execute(sql_query)

        return ActionState.SUCCESS
