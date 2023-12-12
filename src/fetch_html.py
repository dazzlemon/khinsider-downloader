"""
fetch_html.py
"""

from http import HTTPStatus
import requests
from bs4 import BeautifulSoup
from functional import seq


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

        print(f"Failed to retrieve the webpage. Code: {status}")
        return None
    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")
        return None


def extract_hrefs(html_content):
    """
    Extract href values from td elements with class "playlistDownloadSong."
    """
    if html_content is None:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')

    return seq(
        soup.find_all('td', class_='playlistDownloadSong'),
    )\
        .filter(lambda td: td.a)\
        .map(lambda td: td.a['href'])\
        .to_list()
