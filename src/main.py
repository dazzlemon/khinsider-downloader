"""
main.py
"""

import sys
from fetch_html import fetch_html, extract_hrefs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <URL>")
        sys.exit(1)

    URL = sys.argv[1]
    html_content = fetch_html(URL)

    if html_content:
        hrefs = extract_hrefs(html_content)
        print("Extracted HREFs:")
        for href in hrefs:
            print(href)
