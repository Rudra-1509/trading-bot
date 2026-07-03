import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "trading.log")

os.makedirs(LOG_DIR, exist_ok=True)


def setup_logging():

    logging.basicConfig(
        level=logging.INFO,

        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",

        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )