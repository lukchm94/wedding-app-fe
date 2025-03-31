# This file is formatted using black. Run `black /path/to/logger.py` to format manually.

import logging
from logging import Logger

def get_logger(name: str = "wedding-app") -> Logger:
    """
    Returns a configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # Console handler
        
        
        console_handler = logging.StreamHandler()
        
        
        console_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

    return logger


logger: Logger = get_logger()
# Example usage:
# logger.info("This is an info message.")
# logger.error("This is an error message.")
