# -*- coding: utf-8 -*-
import scrapy


class BudejiespiderSpider(scrapy.Spider):
    name = 'budejieSpider'
    allowed_domains = ['budejie.com']
    start_urls = ['http://budejie.com/']

    def parse(self, response):
        pass
