# -*- coding: utf-8 -*-
import scrapy


class XimaspiderSpider(scrapy.Spider):

    name = 'ximaSpider'
    allowed_domains = ['www.ximalaya.com']
    start_urls = ['http://www.ximalaya.com/']

    def parse(self, response):
        pass
