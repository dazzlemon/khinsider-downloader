"""
extract_hrefs.py
"""

from bs4 import BeautifulSoup
from functional import seq


def extract_song_pages_paths(html_content):
    """
    Extract path to pages, where download links are.
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


def extract_download_links(html_content):
    """
    Extract donwload links.
    """
    if html_content is None:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')

    return seq(
        soup.find_all('span', class_='songDownloadLink')
    )\
        .map(lambda span: span.find_previous('a'))\
				.filter(lambda span: span)\
				.map(lambda span: span['href'])\
        .filter(lambda href: href)\
        .to_list()
	