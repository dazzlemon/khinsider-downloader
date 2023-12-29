import scrapy

class Spider(scrapy.Spider):
    name = 'my_spider'

    def start_requests(self):
        start_url = getattr(self, 'start_url', None)
        if not start_url:
            print('Usage: run.(sh|bat) <LINK TO ALBUM> [<ARGUMENTS FOR SCRAPY>]')
        else:
            yield scrapy.Request(url=start_url, callback=self.parse_main_page)

    def parse_main_page(self, response):
        cover_art_links = response.xpath('//div[@class="albumImage"]/a/@href').getall()
        yield {'file_urls': cover_art_links}

        song_pages_paths = response.xpath('//td[@class="playlistDownloadSong"]/a/@href').getall()
        yield from response.follow_all(song_pages_paths, callback=self.parse_song_page)

    def parse_song_page(self, response):
        link = response.xpath('//span[@class="songDownloadLink"]/../@href[re:test(., "\\.flac$")]').get()
        yield {'file_urls': [link]}
