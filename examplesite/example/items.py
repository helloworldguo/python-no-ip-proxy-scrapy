# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JinseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #新闻标题
    title = scrapy.Field();
    #新闻内容
    content = scrapy.Field();
    #新闻链接
    link = scrapy.Field();
    #新闻时间
    time = scrapy.Field();
    pass
