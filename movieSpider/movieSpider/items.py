# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 详情页地址
    url = scrapy.Field()
    # 排名
    rank = scrapy.Field()
    # 名称
    name = scrapy.Field()
    # 别名
    alias = scrapy.Field()
    # 评分
    rating_num = scrapy.Field()
    # 引用标签
    quote = scrapy.Field()
    # pass