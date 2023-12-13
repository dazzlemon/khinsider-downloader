"""
extract_hrefs.py
"""

from bs4 import BeautifulSoup
from functional import seq


def extract_hrefs(html_content, selector, class_name, link_extractor=lambda a: a):
    """
    Extract links based on the provided selector and class.
    """
    if html_content is None:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')

    return seq(
        soup.find_all(selector, class_=class_name)
    )\
			.map(link_extractor)\
			.filter(not_none)\
			.map(lambda a: a['href'])\
			.filter(not_none)\
			.to_list()


def extract_song_pages_paths(html_content):
    """
    Extract path to pages, where download links are.
    """
    def extractor(html_td):
        return html_td.a
    return extract_hrefs(html_content, 'td', 'playlistDownloadSong', extractor)


def extract_download_links(html_content):
    """
    Extract download links.
    """
    def extractor(span):
        return span.find_previous('a')
    return extract_hrefs(html_content, 'span', 'songDownloadLink', extractor)


def not_none(something):
    """
    A short function to use with filter.
    """
    return something is not None
