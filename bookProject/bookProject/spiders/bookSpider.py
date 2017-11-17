# -*- coding: utf-8 -*-
import scrapy


class BookspiderSpider(scrapy.Spider):
    name = 'bookSpider'
    allowed_domains = ['tuzigh.com']
    start_urls = ['http://tuzigh.com/']

    def parse(self, response):
        pass
