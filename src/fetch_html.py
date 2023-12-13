"""
fetch_html.py
"""

from http import HTTPStatus
import requests


def fetch_html(url, timeout=5):
    """
    Fetch HTML content from a given URL.
    """
    try:
        response = requests.get(url, timeout=timeout)
    except requests.exceptions.RequestException as error:
        raise Exception(f'An error occurred: {error}')

    status = response.status_code
    if status != HTTPStatus.OK:
        raise Exception('Failed to retrieve the webpage. Code: {status}')

    html_content = response.text
    if html_content is None:
        raise Exception('Empty html.')

    return html_content
