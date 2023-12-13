"""
main.py
"""

import sys
from functional import seq
from extract_hrefs import extract_download_links, extract_song_pages_paths
from fetch_html import fetch_html, fetch_htmls


def main():
    """
    main
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    html_content = fetch_html(url)

    if not html_content:
        return

    song_pages_paths = extract_song_pages_paths(html_content)
    song_pages_htmls = fetch_htmls(song_pages_paths)

    flac_links = seq(song_pages_htmls)\
        .map(extract_download_links)\
        .map(choose_best_download_link)\
        .to_list()

    for link in flac_links:
        print(link)


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


if __name__ == "__main__":
    main()
