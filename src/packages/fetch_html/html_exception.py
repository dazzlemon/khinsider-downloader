"""
HtmlException
"""


class HtmlException(Exception):
    """
    Exception that might be thrown by [fetch_html].
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
