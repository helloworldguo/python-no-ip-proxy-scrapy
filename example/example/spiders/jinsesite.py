# -*- coding: utf-8 -*-
import scrapy


class ExamplesiteSpider(scrapy.Spider):
    name = 'examplesite'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        # 链接到详情页面
        for href in response.xpath('//div[@class="con index-div"]/ol[@class="list clearfix"]/a/@href').extract():
            yield response.follow(href, self.parse_content_item)

    def parse_content_item(self, response):
        yield{
            'title' : response.xpath('//html/head/title/text()').extract_first(),
            'link' : response._get_url(),
            'content' : response.xpath('//div[@class="con line30 font18"]').extract_first(),
            'time' : response.xpath('//div[@class="time gray5 font12"]/ul/span/text()').extract_first()
        }
