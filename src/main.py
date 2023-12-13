"""
main.py
"""

import sys
import os
from functional import seq
from extract_song_pages import extract_song_pages_paths
from fetch_html import fetch_html, fetch_htmls
from download_links import extract_download_links, choose_best_download_link
from download_file import download_file

def main():
    """
    Entry point.
    """
    if len(sys.argv) != 3:
        print("Usage: python main.py <URL> <SAVE_PATH>")
        sys.exit(1)

    url = sys.argv[1]
    save_path = sys.argv[2]
    html_content = fetch_html(url)

    if not html_content:
        print("Empty html.", file=sys.stderr)
        sys.exit(-1)

    song_pages_paths = extract_song_pages_paths(html_content)
    song_pages_htmls = fetch_htmls(song_pages_paths)

    download_links = seq(song_pages_htmls)\
        .map(extract_download_links)\
        .map(choose_best_download_link)\
        .to_list()

    os.makedirs(save_path, exist_ok=True)

    for link in download_links:
        download_file(link, save_path)


if __name__ == "__main__":
    main()
