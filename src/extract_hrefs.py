"""
extract_hrefs.py
"""

from bs4 import BeautifulSoup
from functional import seq


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
