import os
from urllib.parse import unquote, urlparse
from scrapy.pipelines.files import FilesPipeline
from parfive import Downloader

class MyFilesPipeline(FilesPipeline):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        pipeline = super().from_crawler(crawler, *args, **kwargs)
        cls.FILES_STORE = crawler.settings.get('FILES_STORE')

        return pipeline

    def open_spider(self, spider):
        self.downloader = Downloader()

    def file_path(self, request, response=None, info=None, *, item=None):
        return unquote(os.path.basename(urlparse(request.url).path))

    def process_item(self, item, spider):
        file_url = item.get(self.files_urls_field, [])[0]
        filename = unquote(os.path.basename(urlparse(file_url).path))
        self.downloader.enqueue_file(file_url, filename=filename, path=self.FILES_STORE)

    def close_spider(self, spider):
        self.downloader.download()
