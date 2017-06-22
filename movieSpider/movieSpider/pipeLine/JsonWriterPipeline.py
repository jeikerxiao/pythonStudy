import json
import codecs


class JsonWriterPipeline(object):

    def __init__(self):
        # 解决中文ascii乱码问题
        # self.file = open('movies.json', 'w')
        self.file = codecs.open('movieSpider/download/movies.json', 'w', 'utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        # 解决中文ascii乱码问题
        line_str = line.encode('utf-8').decode('unicode_escape')
        self.file.writelines(line_str)
        return item
