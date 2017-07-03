# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from uuSpider.items import UuspiderItem


class QuanjiSpider(scrapy.Spider):

    name = 'uuSpider'
    allowed_domains = ['uu.com']
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    def start_requests(self):
        return [Request("http://www.uu.com/logging.php?action=login", callback=self.post_login)]

    # 登录表单提交
    def post_login(self, response):
        self.logger.info('---- login start ----')
        # 下面这句代码用于抓取请求网页后返回网页中的 formhash 字段的值, 用于成功提交表单
        formhash = response.xpath('//input[@name="formhash"]/@value').extract()[0]
        self.logger.info('formhash: ' + formhash)
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数
        return [scrapy.FormRequest.from_response(response,
                                          formdata={
                                              'formhash': formhash,
                                              'referer': 'http://www.uu.com/index.php',
                                              'loginfield': 'username',
                                              'username': '账号',
                                              'password': '密码',
                                              'questionid': '0',
                                              'cookietime': '12592000',
                                          },
                                          callback=self.after_login
                                          )]

    # 登录成功后，进入列表分页
    def after_login(self, response):
        self.logger.info('---- login success -----')
        for page_num in range(1, 41, 1):
            url = 'http://www.uu.com/forumdisplay.php?fid=5&page=' + str(page_num)
            yield Request(url, headers=self.headers, callback=self.parse)

    # 解析列表分页上的标题、日期、内容页跳转连接
    def parse(self, response):
        # 将request.content 转化为 Element
        items = response.xpath('//form[@name="moderate"]/*/div[@class="spaceborder"]/table/tr')
        for item in items:
            url_str = 'http://www.uu.com/'+item.xpath('./td[@class="f_title"]/a/@href').extract()[0]
            title_str = ''
            date_str = ''
            try:
                title_str = item.xpath('./td[@class="f_title"]/a/text()').extract()[0]
                date_str = item.xpath('./td[@class="f_last"]/span/a/text()').extract()[0]
            except:
                self.logger.error('get list page failure!')
                pass
            yield Request(url_str, headers=self.headers, callback=self.parseImage, meta={'title': title_str,
                                                                                             'date': date_str})

    # 解析内容页上的 图片url , 传入item。
    def parseImage(self, response):
        title = response.meta['title']
        date = response.meta['date']
        # 将request.content 转化为 Element
        items = response.xpath('//div[@class="t_msgfont"]/img')
        save_item = UuspiderItem()
        for item in items:
            try:
                save_item['title'] = title
                save_item['date'] = date
                save_item['image_urls'] = item.xpath('./@src').extract()
                yield save_item
            except:
                self.logger.error('get content page failure!')
                pass
