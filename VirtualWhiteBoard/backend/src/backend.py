# VirtualWhiteBoard project
from logger.log import get_logger, Logger
from api.api import init_api

logger: Logger = get_logger(__file__)


def main():
    logger.info("Starting backend")
    init_api()


if __name__ == "__main__":
    main()
