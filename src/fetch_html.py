"""
fetch_html.py
"""

import sys
import os
from urllib.parse import unquote
from http import HTTPStatus
import requests
from functional import seq
from util import not_none
from download_file import filename_from_url


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
        .map(fetch_html_from_path)\
        .filter(not_none)\
        .to_list()


def fetch_html_from_path(path):
    """
    Fetch HTML content from a paths.
    """
    url = BASE_URL + path
    filename = unquote(filename_from_url(url))
    songname, _ = os.path.splitext(filename)
    print(f'\t"{songname}"')
    return fetch_html(url)
