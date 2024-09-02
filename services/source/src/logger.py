# This module is responsible to configure the logger
import logging
import sys

__all__ = [
    'setup_logging'
]

def setup_logging(log_file=None, log_level=logging.INFO):
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # If a log file is specified, create a file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger

