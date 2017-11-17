# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import os
import json
import pymysql


class BookprojectPipeline(object):
    def process_item(self, item, spider):
        return item


# 需要在setting.py里设置'coolscrapy.piplines.TxtPipeline':300
class TxtPipeline(object):
    def __init__(self):
        self.file = codecs.open('./data/logs.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        # 从内存以追加的方式打开文件，并写入对应的数据
        if type(item['title']) == str and type(item['url']) == str:
            self.file.write(item['title'] + '\n')
            self.file.write(item['url'] + '\n')
        return item

    def spider_closed(self, spider):
        self.file.close()


# 以下两种写法保存json格式，需要在settings里面设置'coolscrapy.pipelines.JsonPipeline': 200
class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('./data/logs.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if type(item['title']) == str and type(item['url']) == str:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    def process_item(self, item, spider):
        '''
        将爬取的信息保存到mysql
        '''
        # 将item里的数据拿出来
        title = item['title']
        link = item['link']
        posttime = item['posttime']

        # 和本地的newsDB数据库建立连接
        db = pymysql.connect(
            host='localhost',  # 连接的是本地数据库
            user='root',  # 自己的mysql用户名
            passwd='123456',  # 自己的密码
            db='newsDB',  # 数据库的名字
            charset='utf8mb4',  # 默认的编码方式：
            cursorclass=pymysql.cursors.DictCursor)
        try:
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            # SQL 插入语句
            sql = "INSERT INTO NEWS(title,link,posttime) VALUES ('%s', '%s', '%s')" % (title, link, posttime)
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        finally:
            # 关闭连接
            db.close()
        return item
