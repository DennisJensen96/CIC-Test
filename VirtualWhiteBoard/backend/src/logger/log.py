# Standard library
import logging
import os
from logging import Logger

# Third party library
import coloredlogs


def get_logger(logger_name: str):
    logger_name = os.path.basename(logger_name).replace(".py", "")
    logger: str = logging.getLogger(logger_name)

    try:
        log_level: str = os.environ("LOG_LEVEL")
    except TypeError:
        log_level: str = "DEBUG"

    coloredlogs.install(level=log_level, logger=logger)

    return logger
