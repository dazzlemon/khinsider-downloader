import scrapy
import sys
from functional import seq

class MySpider(scrapy.Spider):
    name = 'my_spider'

    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
    }

    def start_requests(self):
        start_url = getattr(self, 'start_url', None)
        if not start_url:
            self.logger.error('Please provide a start URL using the -a start_url=<URL> option')
            sys.exit(1)

        yield scrapy.Request(url=start_url, callback=self.parse_main_page)

    def parse_main_page(self, response):
        cover_art_download_links = response.xpath('//div[@class="albumImage"]/child::a/@href').getall()
        for link in cover_art_download_links:
            print(link)

        song_pages_paths = response.xpath('//td[@class="playlistDownloadSong"]/child::a/@href').getall()
        for path in song_pages_paths:
            yield response.follow(path, callback=self.parse_song_page)

    def parse_song_page(self, response):
        download_links = response.xpath('//span[@class="songDownloadLink"]/parent::a/@href').getall()
        print(self.choose_best_download_link(download_links))

    def choose_best_download_link(self, links):
        """
        Choose flac if any, otherwise take mp3.
        """
        flac_link = next(filter(lambda link: link.endswith('.flac'), links), None)

        return flac_link or next(iter(links), None)