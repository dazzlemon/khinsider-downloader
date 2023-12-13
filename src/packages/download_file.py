"""
download_file.py
"""
import sys
import os
from http import HTTPStatus
from urllib.parse import urlparse, unquote
import requests
from tqdm import tqdm


def filename_from_url(url):
    """
    Extract unescaped filename from url.
    """
    return unquote(os.path.basename(urlparse(url).path))


def download_file(url, destination, chunk_size=12, timeout=600):
    """
    Download file and show progress.
    """
    response = requests.get(url, stream=True, timeout=timeout)

    status = response.status_code
    if status != HTTPStatus.OK:
        print(f'Error when downloading file, status: {status}', file=sys.stderr)
        return

    total_size = int(response.headers.get('content-length', 0))
    with open(destination, 'wb') as file, tqdm(
        desc=os.path.basename(destination),
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        leave=False,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=chunk_size):
            progress_bar.update(len(data))
            file.write(data)
