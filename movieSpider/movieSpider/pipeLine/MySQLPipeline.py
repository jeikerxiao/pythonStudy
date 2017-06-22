# import mysql.connector
import pymysql
import datetime

DEBUG = True

if DEBUG:
    dbuser = 'root'
    dbpass = '123456'
    dbname = 'mydb'
    dbhost = '127.0.0.1'
    dbport = '3306'
else:
    dbuser = 'root'
    dbpass = '123456'
    dbname = 'mydb'
    dbhost = '127.0.0.1'
    dbport = '3306'


class MySQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        # 清空表：
        self.cursor.execute("truncate table douban_spider;")
        self.conn.commit()

    def process_item(self, item, spider):
        curTime = datetime.datetime.now()
        try:
            self.cursor.execute("""INSERT INTO douban_spider (rank, name, alias, rating_num, quote, url, update_time)  
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                (
                                    item['rank'].encode('utf-8'),
                                    item['name'].encode('utf-8'),
                                    item['alias'].encode('utf-8'),
                                    item['rating_num'].encode('utf-8'),
                                    item['quote'].encode('utf-8'),
                                    item['url'].encode('utf-8'),
                                    curTime,
                                )
                                )
            self.conn.commit()
        except Exception as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            pass
        return item
