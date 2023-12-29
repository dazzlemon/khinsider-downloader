import os
from urllib.parse import unquote, urlparse
from pathlib import Path
from scrapy.pipelines.files import FilesPipeline
from parfive import Downloader

class Pipeline(FilesPipeline):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        cls.FILES_STORE = crawler.settings['FILES_STORE']

        return super().from_crawler(crawler, *args, **kwargs)

    def open_spider(self, _): self.downloader = Downloader()

    def process_item(self, item, _):
        path = os.path.join(self.FILES_STORE, item['folder_name'])
        Path(path).mkdir(parents=True, exist_ok=True)
        for url in item['urls']:
            filename = unquote(os.path.basename(urlparse(url).path))
            self.downloader.enqueue_file(url, filename=filename, path=path)

    def close_spider(self, _):
        self.downloader.download()
        print(self.downloader.errors)
