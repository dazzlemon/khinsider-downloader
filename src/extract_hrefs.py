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

    links_elements = seq(
        soup.find_all('td', class_='playlistDownloadSong'),
    )\
			  .map(lambda td: td.a)\
        .to_list()

    return extract_hrefs(links_elements)


def extract_download_links(html_content):
    """
    Extract donwload links.
    """
    if html_content is None:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')

    links_elements = seq(
        soup.find_all('span', class_='songDownloadLink')
    )\
        .map(lambda span: span.find_previous('a'))\
        .to_list()

    return extract_hrefs(links_elements)


def extract_hrefs(links_elements):
    """
    Given a list of <a>'s, extract their hrefs
    """
    return seq(links_elements)\
        .filter(not_none)\
        .map(lambda a: a['href'])\
        .filter(not_none)\
        .to_list()


def not_none(something):
    """
    A short function to use with filter.
    """
    return something is not None
