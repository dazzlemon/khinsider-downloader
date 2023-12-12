"""
MAIN
"""

import sys
from fetch_html import fetch_html

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    URL = sys.argv[1]
    html_content = fetch_html(URL)

    if html_content:
        print(html_content)
