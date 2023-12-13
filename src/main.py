"""
main.py
"""

import sys
import os
from functional import seq
from extract_song_pages import extract_song_pages_paths
from fetch_html import fetch_html, fetch_htmls
from download_links import extract_download_links, choose_best_download_link, extract_covers_links
from download_file import download_file, filename_from_url

def main():
    """
    Entry point.
    """
    if len(sys.argv) != 3:
        print('Usage: python main.py <URL> <SAVE_PATH>')
        sys.exit(1)

    url = sys.argv[1]
    save_path = sys.argv[2]

    print('Fetching main page')
    html_content = fetch_html(url)
    print('')

    if not html_content:
        print('Empty html.', file=sys.stderr)
        sys.exit(-1)

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
        print(f'\t"{filename}"')
        download_file(link, full_path)


if __name__ == "__main__":
    main()
