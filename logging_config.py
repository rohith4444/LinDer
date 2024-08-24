import logging
from logging.handlers import RotatingFileHandler
import os
from config.settings import LOG_LEVEL, LOG_FORMAT, LOG_DIR, MAX_LOG_SIZE, BACKUP_COUNT

# Dictionary to store created loggers
logger_cache = {}

def get_logger(module_name):
    """
    Create and return a logger with both file and console handlers.
    If a logger for the module already exists, return the existing logger.

    :param module_name: Full module name (__name__)
    :return: Configured logger
    """
    # Check if logger already exists
    if module_name in logger_cache:
        return logger_cache[module_name]

    # Split the module name to get the directory and file name
    parts = module_name.split('.')
    if len(parts) > 1:
        # If it's a submodule, use last two parts
        log_file = f"{parts[-2]}.{parts[-1]}.log"
    else:
        # If it's a top-level module, just use the module name
        log_file = f"{module_name}.log"

    logger = logging.getLogger(module_name)
    logger.setLevel(LOG_LEVEL)

    # Only add handlers if they don't exist
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
        console_handler.setLevel(logging.WARNING)  # Only show warnings and errors in console
        logger.addHandler(console_handler)

    # Cache the logger
    logger_cache[module_name] = logger

    return logger

def get_module_logger(module_name):
    """
    Get a logger for a specific module.

    :param module_name: Name of the module (__name__)
    :return: Logger for the specified module
    """
    return get_logger(module_name)