# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from meiwenProject.items import MeiwenprojectItem
from lxml import etree


class NeihanspiderSpider(scrapy.Spider):
    name = 'neihanSpider'
    allowed_domains = ['neihanshequ.com']
    start_urls = ['http://neihanshequ.com/']

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    def start_requests(self):
        # for id in range(1, 10, 1):
        url = 'http://neihanshequ.com'
        yield Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        items = response.xpath("//ul[@id='detail-list']/li")
        for item in items:
            save_item = MeiwenprojectItem()
            save_item['author'] = item.xpath(".//div[@class='name-time-wrapper left']/span[@class='name']/text()").extract_first()
            save_item['date'] = item.xpath(".//span[@class='time']/text()").extract_first()
            save_item['content'] = item.xpath(".//h1[@class='title']/p/text()").extract_first()
            yield save_item
            pass
