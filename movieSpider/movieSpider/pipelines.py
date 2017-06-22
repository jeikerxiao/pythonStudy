# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MoviespiderPipeline(object):
    """
    *清理HTML数据
    *验证爬取的数据(检查item包含某些字段)
    *查重(并丢弃)
    *将爬取结果保存到数据库中    
    """
    def process_item(self, item, spider):
        print(item['name'])
        return item
