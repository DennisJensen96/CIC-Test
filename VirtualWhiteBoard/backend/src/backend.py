# VirtualWhiteBoard project
from logger.log import get_logger, Logger
from database.db_interface import Interface

logger: Logger = get_logger(__file__)


def init_backend():
    logger.info("Testing")
    Interface()


def main():
    logger.info("Starting backend")
    init_backend()


if __name__ == "__main__":
    main()
