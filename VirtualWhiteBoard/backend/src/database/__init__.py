"""[summary]
This module adds the ability to interface with an SQLite3 database
"""

# Standard library
import os
from enum import Enum
import sqlite3
import logging

# Third party libraries
import coloredlogs


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
        self.__logger = logging.getLogger('db')
        coloredlogs.install(level="CRITICAL", logger=self.__logger)
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
        self.__logger = logging.getLogger('db_api')
        coloredlogs.install(level="DEBUG", logger=self.__logger)

    def __del__(self) -> None:
        self._db__connection.close()

    def __create_table(self, website_name: str) -> ActionState:
        sql_query_odds_table = f''' CREATE TABLE IF NOT EXISTS {website_name} (
                                        user_name TEXT PRIMARY KEY NOT NULL,
                                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                                    ); '''

        try:
            self._cursor.execute(sql_query_odds_table)
            return ActionState.SUCCESS
        except Exception as error:
            self.__logger.error(f'Unable to create table error: {error}')
            return ActionState.FAILED
