# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XimaprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    nickname = scrapy.Field()
    play_path = scrapy.Field()
    cover_url = scrapy.Field()
    formatted_created_at = scrapy.Field()
    play_count = scrapy.Field()
    pass
