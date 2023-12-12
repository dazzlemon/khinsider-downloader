"""
main.py
"""

import sys
from extract_hrefs import extract_hrefs
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

    song_pages_paths = extract_hrefs(html_content)

    print("paths:")
    for path in song_pages_paths:
        print(path)
    print("\n")

    song_pages_htmls = fetch_htmls(song_pages_paths)

    print("htmls:")
    for html in song_pages_htmls:
        print(html)

if __name__ == "__main__":
    main()
