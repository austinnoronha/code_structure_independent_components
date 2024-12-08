import logging
import requests
import time
from typing import Any, Dict, Optional

# Utility Functions
def configure_logger(name: str) -> logging.Logger:
    """
    Configures a logger for logging events and errors.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def log_and_trace(logger: logging.Logger, method_name: str, start_time: float, response: Optional[requests.Response] = None):
    """
    Logs and traces the execution time and status of a request.

    Args:
        logger (logging.Logger): Logger instance for logging.
        method_name (str): Name of the method being traced.
        start_time (float): Start time of the request.
        response (Optional[requests.Response]): Response object (default is None).
    """
    elapsed_time = time.time() - start_time
    if response:
        logger.info(f"{method_name} completed in {elapsed_time:.2f}s with status code {response.status_code}")
    else:
        logger.info(f"{method_name} completed in {elapsed_time:.2f}s")
