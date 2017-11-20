# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.http import Request
from bookProject.items import BookprojectItem


class BookspiderSpider(scrapy.Spider):
    # 定义变量
    name = 'bookSpider'
    allowed_domains = ['www.tuzigh.com']
    start_urls = ['http://www.tuzigh.com/']
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/123.36 (KHTML, like Gecko) Chrome/58.0.1231.110 Safari/537.36"
    }

    # 开始爬取列表页
    def start_requests(self):
        for page_num in range(1, 33, 1):
            # 爬取路由规则
            url = 'http://www.tuzigh.com/forum/299653{id}171299380/6{tid}' + str(page_num) + '0178299/6897{name}.html'
            yield Request(url=url, headers=self.headers, callback=self.parse)

    # 解析列表页
    def parse(self, response):
        title_items = response.xpath("//table[@id='threadlisttableid']/*//div[@class='deanflistname']")
        for title_item in title_items:
            title = title_item.xpath("./a/text()").extract_first()
            base_url = title_item.xpath("./a/@href").extract_first()
            content_url = base_url
            print(title)
            print(content_url)
            yield Request(url=content_url, headers=self.headers, callback=self.content_parse)

    # 解析内容页
    def content_parse(self, response):
        logging.info(response.url)
        # 解析标题信息
        title_str = response.xpath("//span[@id='thread_subject']/text()").extract_first()
        mp4_url = response.xpath("//div[@id='postlist']//audio/source/@src").extract_first()
        print(title_str)
        print(mp4_url)
        # 删除标题字符串中的 空格 和 换行符
        item = BookprojectItem()
        item['title'] = response.xpath("//span[@id='thread_subject']/text()").extract_first()
        item['url'] = response.xpath("//audio/source/@src").extract_first()
        yield item
