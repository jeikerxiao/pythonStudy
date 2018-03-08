# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from meiwenProject.items import MeiwenprojectItem

class MeiwenspiderSpider(scrapy.Spider):
    name = 'meiwenSpider'
    allowed_domains = ['meiriyiwen.com']

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    def start_requests(self):
        for id in range(1, 10, 1):
            url = 'http://voice.meiriyiwen.com/voice/show?vid=' + str(id)
            yield Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        save_item = MeiwenprojectItem()

        save_item['title'] = response.xpath("//div[@id='voice_show']/h1[@id='p_title']/text()").extract_first().strip()
        save_item['author'] = response.xpath("//div[@id='voice_show']/p[@class='p_author']/text()").extract_first().strip()
        save_item['url'] = response.xpath("//div[@id='voice_show']/p[@class='p_file']/embed/@src").extract_first()
        yield save_item
        pass
