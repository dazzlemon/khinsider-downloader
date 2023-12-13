"""
extract_song_pages.py
"""
from impl.extract_hrefs import extract_hrefs


def extract_song_pages_paths(html_content):
    """
    Extract path to pages, where download links are.
    """
    def extractor(html_td):
        return html_td.a
    return extract_hrefs(html_content, 'td', 'playlistDownloadSong', extractor)
