import logging
from typing import Any

LOG_FILE = "yt-sorter.log"


def get_logger(log_name: str) -> Any:
    # Create Logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)

    # Create a Formatter
    formatter = logging.Formatter(
        "%(asctime)s [ %(name)s ]  %(levelname)s: %(message)s"
    )

    # Create StreamHandler
    sh = logging.StreamHandler()
    sh.setLevel(logging.WARNING)
    logger.addHandler(sh)

    # Add a fileHandler to debug messages to file
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Hide the eyed3 log noise
    logging.getLogger("eyed3.mp3.headers").setLevel(logging.CRITICAL)

    return logger
