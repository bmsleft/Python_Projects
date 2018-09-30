# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
from subtitle.items import SubtitleItem

class SubTitleSpider(scrapy.Spider):
    name = "subtitle"
    allowed_domains = ["zimuku.net"]
    # start_urls = [
    #     "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=2"
    # ]
    start_urls = []

    def __init__(self):
        self.start_urls = self.get_urls_list()

    def parse(self, response):
        hrefs = response.selector.xpath('//div[contains(@class, "persub")]/h1/a/@href').extract()
        for href in hrefs:
            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        url = response.selector.xpath('//li[contains(@class, "dlsub")]/div/a/@href').extract()[0]
        print "processing: ", url
        request = scrapy.Request(url, callback=self.parse_file)
        yield request

    def parse_file(self, response):
        # print '====parse_file: ====='
        item = SubtitleItem()
        item['url'] = response.url
        item['body'] = response.body
        if response.headers.has_key('Content-Disposition'):
            localName = response.headers['Content-Disposition'].split('filename=')[1]
            if localName[0] == '"' or localName[0] == "'":
                localName = localName[1:-1]
            item['name'] = localName
        else:
            item['name'] = response.url.replace('/', '_').replace(':', '_')
        # print item['name']
        return item


    def get_urls_list(self):
        urlBase = 'http://www.zimuku.net/search?q=&t=onlyst&ad=1&p='
        basePage = 1
        pageCnt = 5000
        urlList = []
        for i in range(basePage, pageCnt + 1):
            urlList.append(urlBase + str(i))
        return urlList