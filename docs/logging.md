# Logging System Documentation

## Overview

This project uses Python's built-in `logging` module to provide comprehensive logging across all components. The logging system is designed to be easy to use and maintain, with features like log rotation to manage log file sizes.

## Configuration

The logging configuration is centralized in the `logging_config.py` file. This file sets up the following:

- Log directory: All log files are stored in a `logs` directory at the root of the project.
- Log level: The default log level is set to `INFO`.
- Log format: Logs include timestamp, logger name, log level, and message.
- Log rotation: Log files are rotated when they reach 5 MB, keeping 5 backup files.

## Usage

To use the logging system in any module:

1. Import the logger at the top of your file:
   ```python
   from logging_config import get_module_logger

   logger = get_module_logger(__name__)
   ```

2. Use the logger throughout your code:
   ```python
   logger.info("This is an informational message")
   logger.warning("This is a warning")
   logger.error("This is an error")
   logger.debug("This is a debug message")
   ```

## Log Files

- Each module has its own log file (e.g., `main.log`, `speech.log`, `text.log`).
- Log files are located in the `logs` directory.
- When a log file reaches 5 MB, it is rotated, and a new file is created.
- Up to 5 old log files are kept before the oldest is deleted.

## Best Practices

1. Use appropriate log levels:
   - DEBUG: Detailed information, typically of interest only when diagnosing problems.
   - INFO: Confirmation that things are working as expected.
   - WARNING: An indication that something unexpected happened, or indicative of some problem in the near future.
   - ERROR: Due to a more serious problem, the software has not been able to perform some function.
   - CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

2. Include relevant information in log messages, such as function parameters or return values when appropriate.

3. Avoid logging sensitive information like passwords or API keys.

4. Use exception logging in try-except blocks:
   ```python
   try:
       # Some code that might raise an exception
   except Exception as e:
       logger.exception(f"An error occurred: {str(e)}")
   ```

## Maintenance

Periodically review and archive old log files to prevent disk space issues. The log rotation policy should handle this automatically, but it's good practice to check occasionally.