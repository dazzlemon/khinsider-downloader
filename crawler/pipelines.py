from scrapy.pipelines.files import FilesPipeline
from urllib.parse import unquote, urlparse
import os

class MyFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return unquote(os.path.basename(urlparse(request.url).path))
