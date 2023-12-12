"""
TODO:
"""

import requests

def fetch_html(url, timeout=5):
    """
    TODO:
    """
    response = requests.get(url, timeout=timeout)

    if response.status_code == 200:
        html_content = response.text
        return html_content

    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return None
