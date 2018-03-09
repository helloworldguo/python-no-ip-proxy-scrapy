# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import re
import pymongo
import time
import random
import logging

class JinsePipeline(object):
    def __init__(self):
        self.filename = open("example.txt", "a+")
        # 建立连接
        uri = "mongodb://xxxxxxx:xxxxxxxx@127.0.0.1:7878/collection_name" 
        self.client = pymongo.MongoClient(uri)
        self.db = self.client['collection_name']

    def check_has_exists(self, db, checklink):
        # 有就返回一个，没有就返回None
        coll = db['document_name']
        result = coll.find_one({"link": checklink})
        return result if result else None

    def insert_one_doc(self, db, title, content, link, nwtime):
        # 插入一个document
        coll = db['news_info']
        information = {"id": int(time.time()), "title": title, "author": "", "seo_keyword": "",
                       "top_parent_category_id": [],"parent_category_id": [], "sub_category_id": [], "tag_info": [], "abstract": "",
                       "allow_comment": 1, "show_homepage": 0,"show_homepage_position": 0, "news_images": "", "content": content,
                       "view_counts": random.randint(100, 400),"comment_counts": 0, "zan_counts": 0, "cai_counts": 0, "link":link,
                       "status": 1, "source":"jinsesite",
                       "origin_create_time": time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(nwtime, "%Y/%m/%d %H:%M")), "create_time":""}
        information_id = coll.insert(information)
        # print(information_id)
        logging.info("information_id rs:" + str(information_id))

    def process_item(self, item, spider):
        title = link = content = time = writeline = ''
        today = datetime.date.today().strftime("%Y/%m/%d %H:%M")
        if item["title"]:
            title = item["title"]
            title = title.replace('\n', '')

        if item["link"]:
            link = item["link"]

        if item["content"]:
            content = item["content"]
            content = content.replace('\r', '')
            content = content.replace('\n', '')
            content = content.replace('\r\n', '')
            dr = re.compile(r'<[^>]+>', re.S)
            content = dr.sub('', content)

        if item["time"]:
            time = item["time"]
        logging.info("origin time:" + time)

        if(time[-3:] == '小时前' or time[-3:] == '分钟前' or time[-3:] == '刚刚'):
            # tmp = time[0:-3]
            # formattime = str(today - datetime.timedelta(hours=int(tmp) + 1))
            formattime = str(today)
        else:
            formattime = time
        logging.info("formattime time:" + formattime)

        if(title and link and content and formattime):
            checkrs = self.check_has_exists(self.db, link)
            logging.info("checkrs:"+str(checkrs))
            if checkrs is None:
                self.insert_one_doc(self.db, title, content, link, formattime)
                writeline += title+"\t"+content+"\t"+link+"\t"+formattime + "\n"
                self.filename.write(writeline)
            else:
                logging.info("logging link has exists:"+link)
        else:
            logging.warning("title or link or content or formattime has empty")
        return item

    def close_spider(self, spider):
        self.filename.close()
