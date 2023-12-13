"""
download_links.py
"""
from functional import seq
from extract_hrefs import extract_hrefs


def extract_download_links(html_content):
    """
    Extract download links.
    """
    def extractor(span):
        return span.find_previous('a')
    return extract_hrefs(html_content, 'span', 'songDownloadLink', extractor)


def choose_best_download_link(links):
    """
    Choose flac if any, otherwise take mp3.
    """
    if len(links) == 0:
        return None

    flac_links = seq(links)\
        .filter(lambda link: link.endswith('.flac'))\
        .to_list()

    if len(flac_links) == 0:
        return links[0]

    return flac_links[0]
