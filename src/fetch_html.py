"""
fetch_html.py
"""

import sys
from http import HTTPStatus
import requests
from functional import seq


BASE_URL = 'https://downloads.khinsider.com'


def fetch_html(url, timeout=5):
    """
    Fetch HTML content from a given URL.
    """
    try:
        response = requests.get(url, timeout=timeout)

        status = response.status_code
        if status == HTTPStatus.OK:
            html_content = response.text
            return html_content

        print(f"Failed to retrieve the webpage. Code: {status}", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}", file=sys.stderr)
        return None


def fetch_htmls(paths):
    """
    Fetch HTML content from a list of paths.
    """
    return seq(paths)\
        .map(lambda path: fetch_html(BASE_URL + path))\
        .filter(lambda html: html)\
        .to_list()
