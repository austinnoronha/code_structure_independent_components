import logging
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import time

from abstract_api_collector import configure_logger, log_and_trace  # Reused utilities


class AbstractScraper(ABC):
    """
    Abstract base class for web scrapers.
    This class provides foundational functionality for:
    - HTTP request handling.
    - Parsing HTML responses.
    - Error handling and logging.
    """

    def __init__(self, base_url: str, user_agent: Optional[str] = None, proxies: Optional[Dict[str, str]] = None):
        """
        Initialize the scraper.

        Args:
            base_url (str): Base URL for the target website.
            user_agent (Optional[str]): Custom User-Agent for the scraper (default is None).
            proxies (Optional[Dict[str, str]]): Proxy settings for requests (default is None).
        """
        self.base_url = base_url
        self.user_agent = user_agent or "Mozilla/5.0 (compatible; AbstractScraper/1.0)"
        self.proxies = proxies
        self.session = self._configure_session()
        self.logger = configure_logger(self.__class__.__name__)

    def _configure_session(self) -> requests.Session:
        """
        Configures the requests session with headers and proxy settings.

        Returns:
            requests.Session: Configured session.
        """
        session = requests.Session()
        session.headers.update({"User-Agent": self.user_agent})
        if self.proxies:
            session.proxies.update(self.proxies)
        return session

    def _fetch_page(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Fetches a page's HTML content.

        Args:
            endpoint (str): Endpoint or path to scrape.
            params (Optional[Dict[str, Any]]): Query parameters (default is None).

        Returns:
            str: HTML content of the page.

        Raises:
            requests.RequestException: If the request fails.
        """
        url = f"{self.base_url}/{endpoint}"
        start_time = time.time()
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            log_and_trace(self.logger, "_fetch_page", start_time, response)
            return response.text
        except requests.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred while fetching page: {http_err}")
            raise
        except requests.RequestException as req_err:
            self.logger.error(f"Request error occurred while fetching page: {req_err}")
            raise

    def _parse_html(self, html_content: str) -> BeautifulSoup:
        """
        Parses HTML content using BeautifulSoup.

        Args:
            html_content (str): HTML content to parse.

        Returns:
            BeautifulSoup: Parsed HTML content.

        Raises:
            ValueError: If the HTML content is invalid.
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            return soup
        except Exception as err:
            self.logger.error(f"Error while parsing HTML: {err}")
            raise ValueError(f"Invalid HTML content: {err}")

    @abstractmethod
    def scrape(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
        """
        Abstract method to scrape data from the website.

        Args:
            endpoint (str): Endpoint or path to scrape.
            params (Optional[Dict[str, Any]]): Query parameters (default is None).
        """
        pass


# #Example Implementation of a Subclass
# class ExampleScraper(AbstractScraper):
#     def scrape(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
#         """
#         Scrapes data from the given endpoint.

#         Args:
#             endpoint (str): Path to scrape.
#             params (Optional[Dict[str, Any]]): Query parameters for the request.

#         Returns:
#             Dict[str, Any]: Scraped data.
#         """
#         html_content = self._fetch_page(endpoint, params)
#         soup = self._parse_html(html_content)
#         # Example: Extracting all links
#         links = [a['href'] for a in soup.find_all('a', href=True)]
#         return {"links": links}
