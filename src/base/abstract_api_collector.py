import requests
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from src.utils.logging import configure_logger, log_and_trace

# Abstract Base Class
class AbstractAPICollector(ABC):
    """
    Abstract base class for REST API collectors.
    This class provides foundational functionality to interact with REST APIs, including:
    - Configuration setup for authentication.
    - Common request handling for GET/POST methods.
    - Error handling for robustness.
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the API collector.

        Args:
            base_url (str): Base URL for the API.
            api_key (Optional[str]): API key for authentication (default is None).
            username (Optional[str]): Username for basic auth (default is None).
            password (Optional[str]): Password for basic auth (default is None).
        """
        self.base_url = base_url
        self.api_key = api_key
        self.username = username
        self.password = password
        self.session = self._configure_session()
        self.logger = configure_logger(self.__class__.__name__)

    def _configure_session(self) -> requests.Session:
        """
        Configures the requests session for API interaction.

        Returns:
            requests.Session: Configured session with appropriate headers or authentication.
        """
        session = requests.Session()
        if self.api_key:
            session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        if self.username and self.password:
            session.auth = (self.username, self.password)
        return session

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Internal method to make HTTP requests.

        Args:
            method (str): HTTP method ('GET', 'POST', etc.).
            endpoint (str): API endpoint to call.
            params (Optional[Dict[str, Any]]): Query parameters (default is None).
            data (Optional[Dict[str, Any]]): Request body for POST/PUT requests (default is None).

        Returns:
            Dict[str, Any]: Parsed JSON response.

        Raises:
            requests.RequestException: If the request fails or the response is invalid.
        """
        url = f"{self.base_url}/{endpoint}"
        start_time = time.time()
        try:
            response = self.session.request(method, url, params=params, json=data)
            response.raise_for_status()
            log_and_trace(self.logger, "_make_request", start_time, response)
            return response.json()
        except requests.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise
        except requests.RequestException as req_err:
            self.logger.error(f"Request error occurred: {req_err}")
            raise
        except Exception as err:
            self.logger.error(f"Unexpected error: {err}")
            raise

    @abstractmethod
    def fetch_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
        """
        Abstract method to fetch data from the API.

        Args:
            endpoint (str): API endpoint.
            params (Optional[Dict[str, Any]]): Query parameters for the request (default is None).
        """
        pass
