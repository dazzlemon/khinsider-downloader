"""
download_file.py
"""
import os
from urllib.parse import urlparse, unquote
import requests


def download_file(url, local_directory, timeout=600):
    """
    Download a file from the given URL and save it in the specified local directory.
    """
    response = requests.get(url, stream=True, timeout=timeout)
    filename = unquote(os.path.basename(urlparse(url).path))
    full_path = os.path.join(local_directory, filename)

    print(f'Downloading "{filename}"')

    with open(full_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
