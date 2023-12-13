"""
fetch_html.py
"""

from http import HTTPStatus
import requests
from .html_exception import HtmlException
from .empty_html_exception import EmptyHtmlException


def fetch_html(url, timeout=5):
    """
    Fetch HTML content from a given URL.
    """
    try:
        response = requests.get(url, timeout=timeout)
    except requests.exceptions.RequestException as error:
        raise HtmlException('An error occurred') from error

    status = response.status_code
    if status != HTTPStatus.OK:
        raise HtmlException('Failed to retrieve the webpage. Code: {status}')

    html_content = response.text
    if html_content is None:
        raise EmptyHtmlException()

    return html_content
