"""
extract_hrefs.py
"""

from bs4 import BeautifulSoup
from functional import seq
from packages.util import not_none


def extract_hrefs(html_content, selector, class_name, link_extractor=lambda a: a):
    """
    Extract links based on the provided selector and class.
    """
    elements = BeautifulSoup(html_content, 'html.parser')\
        .find_all(selector, class_=class_name)

    return seq(elements)\
        .map(link_extractor)\
        .filter(not_none)\
        .map(lambda a: a['href'])\
        .filter(not_none)\
        .to_list()
