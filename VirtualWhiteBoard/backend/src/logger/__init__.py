# Standard library
import logging
import os

# Third party library
import coloredlogs


def get_logger(logger_name: str):
    logger_name = os.path.basename(logger_name).replace(".py", "")
    logger: str = logging.getLogger(logger_name)
    log_level: str = os.environ("LOG_LEVEL")
    coloredlogs.install(level=log_level, logger=logger)

    return logger
