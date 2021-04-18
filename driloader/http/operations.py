# pylint: disable=no-member
"""
Holds the classes that implement HTTP operations.
"""
import requests

from requests_html import HTMLSession
from urllib3.exceptions import InsecureRequestWarning


class HttpOperations:
    """
    Exposes methods to interact with URLs.
    """

    def __init__(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    @staticmethod
    def get(url, params=None, verify=False, proxies=None):
        """
        Performs a GET request and returns a Response class.
        """
        return requests.get(url, params=params, verify=verify, proxies=proxies)

    @staticmethod
    def get_html(url):
        """
        Performs a GET in a html page and returns the HTML.
        """
        return HTMLSession().get(url)
