# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.http import Request


class XimaspiderSpider(scrapy.Spider):

    name = 'ximaSpider'
    allowed_domains = ['www.ximalaya.com']
    start_urls = ['http://www.ximalaya.com/']
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/123.36 (KHTML, like Gecko) Chrome/58.0.1231.110 Safari/537.36"
    }

    # 开始爬取列表页
    def start_requests(self):
        for page_num in range(1, 10, 1):
            # 爬取路由规则
            url = 'http://www.ximalaya.com/dq/' + str(page_num)
            yield Request(url=url, headers=self.headers, callback=self.parse)

    # 解析列表页
    def parse(self, response):
        logging.info(response.url)
        pass
