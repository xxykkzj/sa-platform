"""
HTML helper methods
"""

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from helpers.string_helper import StringHelper


class UrlHelper:
    """
    HTML Helper
    """

    def __init__(self) -> None:
        self.string_helper = StringHelper()

    def is_valid_url(self, url: str):
        """
        Check if url is valid
        """
        if self.string_helper.is_null_or_whitespace(url):
            return False

        url = url.strip()
        if not url.startswith("http"):
            return False

        return True

    def find_urls(self, html: str):
        """
        Find urls from the html
        """
        self.string_helper.validate_null_or_empty(html, "html")
        soup = BeautifulSoup(html, "html.parser")
        anchor_tags = soup.findAll("a")
        return list(
            {a.get("href")
             for a in anchor_tags if self.is_valid_url(a.get("href"))}
        )

    def get_domain(self, url: str):
        """get domain of url"""
        return urlparse(url).netloc

    def remove_query_params(self, url: str):
        """remove query parameters"""
        return urljoin(url, urlparse(url).path)
