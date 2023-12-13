"""
download_links.py
"""
from impl.extract_hrefs import extract_hrefs


def extract_download_links(html_content):
    """
    Extract download links for songs.
    """
    return extract_hrefs(
        html_content,
        'span',
        'songDownloadLink',
        lambda span: span.find_previous('a'),
    )


def extract_covers_links(html_content):
    """
    Extract download links for covers.
    """
    return extract_hrefs(html_content, 'div', 'albumImage', lambda div: div.a)


def choose_best_download_link(links):
    """
    Choose flac if any, otherwise take mp3.
    """
    flac_link = next(filter(lambda link: link.endswith('.flac'), links), None)

    return flac_link or next(iter(links), None)
