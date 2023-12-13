"""
main.py
"""

import sys
import os
from functional import seq
from impl.extract_song_pages import extract_song_pages_paths

from impl.download_links import (
    extract_download_links,
    choose_best_download_link,
    extract_covers_links
)

from packages.download_file import download_file, filename_from_url
from cli.fetch_html import fetch_htmls, fetch_main_page


def main():
    """
    Entry point.
    """
    if len(sys.argv) != 3:
        print('Usage: python main.py <URL> <SAVE_PATH>')
        sys.exit(-1)

    url = sys.argv[1]
    save_path = sys.argv[2]

    html_content = fetch_main_page(url)
    covers_links = extract_covers_links_cli(html_content)
    song_pages_paths = extract_song_pages_paths_cli(html_content)
    download_links = get_song_download_links(song_pages_paths)
    download(save_path, download_links + covers_links)


def extract_covers_links_cli(html_content):
    print('Scraping cover art links', end='')
    covers_links = extract_covers_links(html_content)
    print(f' - Got {len(covers_links)}\n')
    return covers_links


def extract_song_pages_paths_cli(html_content):
    print('Scraping song pages links', end='')
    song_pages_paths = extract_song_pages_paths(html_content)
    print(f' - Got {len(song_pages_paths)}\n')
    return song_pages_paths


def get_song_download_links(song_pages_paths):
    print('Scraping song download links')
    song_pages_htmls = fetch_htmls(song_pages_paths)

    download_links = seq(song_pages_htmls)\
        .map(extract_download_links)\
        .map(choose_best_download_link)\
        .to_list()
    print('')
    return download_links


def download(save_path, links):
    print("Downloading:")
    os.makedirs(save_path, exist_ok=True)

    for link in links:
        filename = filename_from_url(link)
        full_path = os.path.join(save_path, filename)
        print(f'\t{filename}')
        download_file(link, full_path)


if __name__ == "__main__":
    main()
