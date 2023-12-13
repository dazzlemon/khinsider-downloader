"""
main.py
"""

import sys
import os
from urllib.parse import unquote
from functional import seq
from extract_song_pages import extract_song_pages_paths
from fetch_html import fetch_html
from download_links import extract_download_links, choose_best_download_link, extract_covers_links
from download_file import download_file, filename_from_url
from util import not_none

def main():
    """
    Entry point.
    """
    if len(sys.argv) != 3:
        print('Usage: python main.py <URL> <SAVE_PATH>')
        sys.exit(-1)

    url = sys.argv[1]
    save_path = sys.argv[2]

    print('Fetching main page')
    try:
        html_content = fetch_html(url)
    except Exception as error:
        print(error, file=sys.stderr)
        sys.exit(-1)
    print('')

    print('Scraping cover art links', end='')
    covers_links = extract_covers_links(html_content)
    print(f' - Got {len(covers_links)}\n')

    print('Scraping song pages links', end='')
    song_pages_paths = extract_song_pages_paths(html_content)
    print(f' - Got {len(song_pages_paths)}\n')

    print('Scraping song download links')
    song_pages_htmls = fetch_htmls(song_pages_paths)

    download_links = seq(song_pages_htmls)\
        .map(extract_download_links)\
        .map(choose_best_download_link)\
        .to_list()
    print('')

    print("Downloading:")
    os.makedirs(save_path, exist_ok=True)

    for link in download_links + covers_links:
        filename = filename_from_url(link)
        full_path = os.path.join(save_path, filename)
        print(f'\t{filename}')
        download_file(link, full_path)


BASE_URL = 'https://downloads.khinsider.com'


def fetch_htmls(paths):
    """
    Fetch HTML content from a list of paths.
    """
    return seq(paths)\
        .map(fetch_html_from_path)\
        .filter(not_none)\
        .to_list()


def fetch_html_from_path(path):
    """
    Fetch HTML content from a paths.
    """
    url = BASE_URL + path
    filename = unquote(filename_from_url(url))
    songname, _ = os.path.splitext(filename)
    print(f'\t{songname}')
    return fetch_html(url)


if __name__ == "__main__":
    main()
