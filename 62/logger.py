import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_DIR = 'logs'
LOG_FILE = 'cafe.log'
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str = __name__) -> logging.Logger:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s -%(funcName)s %(message)s'
    )

    # console logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # file logging
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, LOG_FILE),
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8',
        utc=False
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger