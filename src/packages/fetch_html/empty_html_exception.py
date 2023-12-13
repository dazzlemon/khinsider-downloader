"""
EmptyHtmlException
"""
from .html_exception import HtmlException


class EmptyHtmlException(HtmlException):
    """
    A more specific case of [HtmlException]
    """
    def __init__(self):
        super().__init__('Empty html.')
