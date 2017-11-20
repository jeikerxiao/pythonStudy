# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

class XimaprojectPipeline(object):
    def process_item(self, item, spider):
        return item


# 需要在setting.py里设置'coolscrapy.piplines.TxtPipeline':300
class TxtPipeline(object):
    def __init__(self):
        self.file = codecs.open('./data/logs.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 从内存以追加的方式打开文件，并写入对应的数据
        if type(item['title']) == str and type(item['nickname']) == str:
            self.file.write('------------------------------' + '\n')
            self.file.write('标题：' + item['title'] + '\n')
            self.file.write('昵称：' + item['nickname'] + '\n')
            self.file.write('音频路径：' + item['play_path'] + '\n')
            self.file.write('图片路径：' + item['cover_url'] + '\n')
            self.file.write('创建时间：' + item['formatted_created_at'] + '\n')
        return item

    def spider_closed(self, spider):
        self.file.close()


# 以下两种写法保存json格式，需要在settings里面设置'coolscrapy.pipelines.JsonPipeline': 200
class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('./data/logs.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if type(item['title']) == str and type(item['nickname']) == str:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()