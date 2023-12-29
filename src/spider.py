import scrapy

class Spider(scrapy.Spider):
    name = 'my_spider'

    def start_requests(self):
        file_path = getattr(self, 'file_path', None)
        if not file_path:
            print('Usage: run.(sh|bat) <FILE WITH LINKS TO ALBUMS> [<ARGUMENTS FOR SCRAPY>]')
            return

        with open(file_path, 'r') as file:
            urls = file.readlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_main_page)

    def parse_main_page(self, response):
        album_name = response.xpath('//div[@id="pageContent"]/h2/text()').get()
        year = response.xpath('//div[@id="pageContent"]/p[@align="left"]/b/text()').get()
        folder_name = f'{year} - {album_name}'
        
        cover_art_links = response.xpath('//div[@class="albumImage"]/a/@href').getall()
        yield {'urls': cover_art_links, 'folder_name': folder_name}

        song_pages_paths = response.xpath('//td[@class="playlistDownloadSong"]/a/@href').getall()
        yield from response.follow_all(song_pages_paths, callback=self.parse_song_page, cb_kwargs={'folder_name': folder_name})

    def parse_song_page(self, response, **kwargs):
        link = response.xpath('//span[@class="songDownloadLink"]/../@href[re:test(., "\\.flac$")]').get()
        yield {'urls': [link], **kwargs}
