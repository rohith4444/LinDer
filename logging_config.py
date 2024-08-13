import logging
from logging.handlers import RotatingFileHandler
import os
from config.settings import LOG_LEVEL, LOG_FORMAT, LOG_DIR, MAX_LOG_SIZE, BACKUP_COUNT

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
        # File Handler with rotation
        os.makedirs(LOG_DIR, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(LOG_DIR, log_file),
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT
        )
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
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

