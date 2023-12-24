"""
main.py
"""

import sys
import shutil
import os
import multiprocessing
from urllib.parse import unquote, urlparse
from parfive import Downloader

from impl.extract_song_pages import extract_song_pages_paths

from impl.download_links import (
    extract_download_links,
    choose_best_download_link,
    extract_covers_links
)

from packages.util import not_none
from packages.fetch_html import fetch_html, HtmlException


BASE_URL = 'https://downloads.khinsider.com'


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
    song_pages_paths = extract_song_pages_paths(html_content)
    download_links = get_song_download_links(song_pages_paths)
    download(save_path, download_links + covers_links)


def fetch_main_page(url):
    """
    Fetch main page.
    """
    print('Fetching main page')
    try:
        return fetch_html(url)
    except HtmlException as error:
        print(error.message, file=sys.stderr)
        sys.exit(-1)


def clear_line():
    columns, _ = shutil.get_terminal_size()
    print(' ' * columns, end='\r')


def extract_covers_links_cli(html_content):
    print('Scraping cover art links', end='')
    covers_links = extract_covers_links(html_content)
    print(f' - Got {len(covers_links)}')
    return covers_links


def get_song_download_links(song_pages_paths):
    print('Scraping song download links', end='\r')

    with multiprocessing.Pool() as pool:
        download_links = pool.map(process_song_page, song_pages_paths)

    errors, download_links = list(zip(*download_links))
    errors = list(filter(not_none, errors))
    download_links = list(filter(not_none, download_links))

    clear_line()
    print(f'Scraping song download links - Got {len(download_links)}')

    for error in errors:
        print(error.message, file=sys.stderr)

    return download_links


def process_song_page(path):
    try:
        html_content = fetch_html(BASE_URL + path)
        download_links = extract_download_links(html_content)

        return None, choose_best_download_link(download_links)
    except HtmlException as error:
        return error, None


def download(save_path, links):
    os.makedirs(save_path, exist_ok=True)
    downloader = Downloader()

    for link in links:
        filename = unquote(os.path.basename(urlparse(link).path))
        downloader.enqueue_file(link, path=save_path, filename=filename)

    downloader.download()


if __name__ == "__main__":
    main()
