"""
download_file.py
"""
import os
from urllib.parse import urlparse, unquote
import requests


def download_file(url, save_path, timeout=600):
    """
    Download a file from the given URL and save it in the specified local directory.
    """
    response = requests.get(url, stream=True, timeout=timeout)

    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


def filename_from_url(url):
    """
    Extract unescaped filename from url.
    """
    return unquote(os.path.basename(urlparse(url).path))
