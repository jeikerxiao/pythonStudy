import scrapy
from lxml import etree
from scrapy.http import Request
from movieSpider.items import MovieSpiderItem
# from movieSpider.movieSpider.pipeLine.MySQLPipeline import MySQLPipeline
# from ..pipeLine.MySQLPipeline import MySQLPipeline


class Myspider(scrapy.Spider):
    name = 'movieSpider'
    allowed_domains = ['douban.com']
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    def start_requests(self):
        for id in range(0, 251, 25):
            url = 'https://movie.douban.com/top250?start=' + str(id)
            yield Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        # 将request.content 转化为 Element
        root = etree.HTML(response.text)
        # 选取 ol/li/div[@class="item"] 不管它们在文档中的位置
        items = root.xpath('//ol/li/div[@class="item"]')
        for item in items:
            # 注意可能只有中文名，没有英文名；可能没有quote简评
            rank, name, alias, rating_num, quote, url = "", "", "", "", "", ""
            try:
                save_item = MovieSpiderItem()
                save_item['url'] = item.xpath('./div[@class="pic"]/a/@href')[0]
                save_item['rank'] = item.xpath('./div[@class="pic"]/em/text()')[0]
                title = item.xpath('./div[@class="info"]//a/span[@class="title"]/text()')
                save_item['name'] = title[0].encode('gb2312', 'ignore').decode('gb2312')

                save_item['alias'] = title[1].encode('gb2312', 'ignore').decode('gb2312') if len(title) == 2 else ""
                save_item['rating_num'] = item.xpath('.//div[@class="bd"]//span[@class="rating_num"]/text()')[0]
                quote_tag = item.xpath('.//div[@class="bd"]//span[@class="inq"]')
                if len(quote_tag) is not 0:
                    save_item['quote'] = quote_tag[0].text.encode('gb2312', 'ignore').decode('gb2312').replace('\xa0', '')
                # 输出 排名，评分，简介
                # print(rank, rating_num, quote)
                # 输出 中文名，英文名
                # print(name.encode('gb2312', 'ignore').decode('gb2312'),
                #       alias.encode('gb2312', 'ignore').decode('gb2312').replace('/', ','))
                yield save_item
            except:
                print('faild!')
                pass
