"""
main.py
"""

import sys
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

    for html in song_pages_htmls:
        song_download_links = extract_download_links(html)
        for link in song_download_links:
            print(link)

if __name__ == "__main__":
    main()
