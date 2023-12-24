import scrapy

class MySpider(scrapy.Spider):
    name = 'my_spider'

    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'ITEM_PIPELINES': {
            'scrapy.pipelines.files.FilesPipeline': 1,
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_url = kwargs.get('start_url')
        self.links = []
        self.custom_settings['FILES_STORE'] = kwargs.get('path', None)

    def start_requests(self):
        if not self.start_url or not self.custom_settings['FILES_STORE']:
            print(
                'Usage: scrapy runspider myspider.py '
                '-a start_url=<URL> '
                '-a path=<PATH>'
            )
        else:
            yield scrapy.Request(url=self.start_url, callback=self.parse_main_page)

    def parse_main_page(self, response):
        cover_art_links = response.xpath('//div[@class="albumImage"]/a/@href').getall()
        for link in cover_art_links:
            yield {'file_urls': [link]}

        song_pages_paths = response.xpath('//td[@class="playlistDownloadSong"]/a/@href').getall()
        for path in song_pages_paths:
            yield response.follow(path, callback=self.parse_song_page)

    def parse_song_page(self, response):
        links = response.xpath('//span[@class="songDownloadLink"]/../@href').getall()
        flac_link = next(filter(lambda link: link.endswith('.flac'), links), None)
        yield {'file_urls': [flac_link or next(iter(links), None)]}
