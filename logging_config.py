# File: logging_config.py

import logging
import os
from logging.handlers import RotatingFileHandler

# Get the root directory of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define log directory
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Define log levels
LOG_LEVEL = logging.INFO

# Define log format
LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_logger(name, log_file):
    """
    Create and return a logger with both file and console handlers.

    :param name: Name of the logger (usually __name__)
    :param log_file: Name of the log file
    :return: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Prevent adding handlers if they already exist
    if not logger.handlers:
        # File Handler
        file_handler = RotatingFileHandler(
            os.path.join(LOG_DIR, log_file),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(LOG_FORMAT)
        logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(LOG_FORMAT)
        logger.addHandler(console_handler)

    return logger

# Create loggers for different modules
main_logger = get_logger('main', 'main.log')
speech_logger = get_logger('speech', 'speech.log')
text_logger = get_logger('text', 'text.log')
utils_logger = get_logger('utils', 'utils.log')

# Function to get logger by name
def get_module_logger(module_name):
    """
    Get a logger for a specific module.

    :param module_name: Name of the module
    :return: Logger for the specified module
    """
    if module_name == 'main':
        return main_logger
    elif module_name == 'speech':
        return speech_logger
    elif module_name == 'text':
        return text_logger
    elif module_name == 'utils':
        return utils_logger
    else:
        # If an unknown module is requested, create a new logger
        return get_logger(module_name, f'{module_name}.log')

# Example usage in other files:
# from logging_config import get_module_logger
# logger = get_module_logger(__name__)