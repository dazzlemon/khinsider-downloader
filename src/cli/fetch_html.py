"""
fetch_html cli.
"""
import sys
import os
from urllib.parse import unquote
from functional import seq
from packages.util import not_none
from packages.download_file import filename_from_url
from packages.fetch_html import fetch_html, HtmlException


BASE_URL = 'https://downloads.khinsider.com'


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
    print(f'\t{songname}')
    try:
        return fetch_html(url)
    except HtmlException as error:
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
    print('')
    return html_content
