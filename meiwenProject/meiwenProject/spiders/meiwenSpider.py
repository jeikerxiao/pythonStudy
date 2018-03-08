# -*- coding: utf-8 -*-
import scrapy


class MeiwenspiderSpider(scrapy.Spider):
    name = 'meiwenSpider'
    allowed_domains = ['meiriyiwen.com']
    start_urls = ['http://meiriyiwen.com/']

    def parse(self, response):
        pass
