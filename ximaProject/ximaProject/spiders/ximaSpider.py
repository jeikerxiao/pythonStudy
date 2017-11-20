# -*- coding: utf-8 -*-
import scrapy
import logging
import json
from scrapy.http import Request
from ximaProject.items import XimaprojectItem


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
            url = 'http://www.ximalaya.com/dq/' + str(page_num) + '/'
            yield Request(url=url, headers=self.headers, callback=self.parse)

    # 解析列表页
    def parse(self, response):
        logging.info(response.url)
        album_items = response.xpath("//div[@id='explore_album_detail_entry']/div[@class='discoverAlbum_wrapper']/div[@class='discoverAlbum_item']")
        for album in album_items:
            album_title = album.xpath("./a[@class='discoverAlbum_title']/text()").extract_first()
            album_url = album.xpath("./a[@class='discoverAlbum_title']/@href").extract_first()
            album_image_url = album.xpath("//a[@class='albumface']/span/img/@src").extract_first()
            album_play_count = album.xpath("//span[@class='sound_playcount']/text()").extract_first()
            logging.info(album_title)
            logging.info(album_url)
            yield Request(url=album_url, headers=self.headers, callback=self.content_parse)


    # 解析内容页
    def content_parse(self, response):
        logging.info(response.url)
        # 解析标题信息
        sound_ids = response.xpath('//div[@class="personal_body"]/@sound_ids').extract_first().split(',')
        for i in sound_ids:
            sound_json_url = 'http://www.ximalaya.com/tracks/{}.json'.format(i)
            yield Request(url=sound_json_url, headers=self.headers, callback=self.json_parse)

    def json_parse(self, response):
        sound_dic = json.loads(response.body)

        # 删除标题字符串中的 空格 和 换行符
        item = XimaprojectItem()
        item['title'] = sound_dic['title']
        item['nickname'] = sound_dic['nickname']
        item['play_path'] = sound_dic['play_path']
        item['cover_url'] = sound_dic['cover_url']
        item['formatted_created_at'] = sound_dic['formatted_created_at']

        yield item