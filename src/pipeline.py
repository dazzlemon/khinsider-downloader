import os
from urllib.parse import unquote, urlparse
from scrapy.pipelines.files import FilesPipeline
from parfive import Downloader

class Pipeline(FilesPipeline):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        cls.FILES_STORE = crawler.settings['FILES_STORE']

        return super().from_crawler(crawler, *args, **kwargs)

    def open_spider(self, _): self.downloader = Downloader()

    def process_item(self, item, _):
        for url in item[self.files_urls_field]:
            filename = unquote(os.path.basename(urlparse(url).path))
            self.downloader.enqueue_file(url, filename=filename, path=self.FILES_STORE)

    def close_spider(self, _): self.downloader.download()
