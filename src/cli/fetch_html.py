"""
fetch_html cli.
"""
import sys
import shutil
from packages.fetch_html import fetch_html, HtmlException


BASE_URL = 'https://downloads.khinsider.com'


def fetch_html_from_path(path):
    """
    Fetch HTML content from a paths.
    """
    url = BASE_URL + path
    try:
        return fetch_html(url)
    except HtmlException as error:
        # TODO: improve
        print(error.message, file=sys.stderr)
        return None


def fetch_main_page(url):
    """
    Fetch main page.
    """
    print('Fetching main page')
    try:
        html_content = fetch_html(url)
    except HtmlException as error:
        print(error.message, file=sys.stderr)
        sys.exit(-1)
    return html_content


def clear_line():
    columns, _ = shutil.get_terminal_size()
    print(' ' * columns, end='\r')
