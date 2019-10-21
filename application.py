import logging
from logging.handlers import RotatingFileHandler

from app import app as application


if __name__ == '__main__':

    log_handler = RotatingFileHandler('info.log', maxBytes=2000, backupCount=1)

    log_handler.setLevel(logging.INFO)

    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_handler.setFormatter(logger_formatter)

    application.logger.setLevel(logging.INFO)

    application.logger.addHandler(log_handler)

    application.run(host='0.0.0.0')