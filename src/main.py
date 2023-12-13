"""
main.py
"""

import sys
from functional import seq
from extract_song_pages import extract_song_pages_paths
from fetch_html import fetch_html, fetch_htmls
from download_links import extract_download_links, choose_best_download_link

def main():
    """
    Entry point.
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


if __name__ == "__main__":
    main()
