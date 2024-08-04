import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ApplicationError(Exception):
    """Base class for application-specific errors."""
    pass

class APIError(ApplicationError):
    """Raised when an API call fails."""
    pass

class InputError(ApplicationError):
    """Raised when user input is invalid."""
    pass

def handle_error(error, error_type=None):
    """
    Handles errors by logging them and optionally re-raising.
    
    :param error: The error that occurred
    :param error_type: Optional custom error type to raise
    """
    logging.error(f"An error occurred: {str(error)}")
    
    if error_type:
        raise error_type(str(error))
    else:
        raise error

# Example usage:
# try:
#     # Some code that might raise an exception
#     raise ValueError("Something went wrong")
# except ValueError as e:
#     handle_error(e, APIError)