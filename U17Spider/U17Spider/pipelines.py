# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymongo
import pymysql
import urllib.request

from U17Spider.items import U17ImagesItem, U17SpiderItem
from U17Spider.settings import MONGODB_PORT, MONGODB_HOST


class U17SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline():

    def __init__(self, mongodb_host, mongodb_port):
        self.host = mongodb_host,
        self.port = mongodb_port

    def process_item(self, item, spider):
        if isinstance(item, U17SpiderItem):
            # try:
            #     self.db['all_novels'].insert(dict(item))
            # except:
            #     print(f'{item["name"]}写入出错...')
            pass
        return item

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            host=self.host,
            port=self.port
        )
        self.db = self.client['u17_data']

    def close_spider(self, spider):
        self.client.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_host = MONGODB_HOST,
            mongodb_port = MONGODB_PORT
        )


class MySQLPipeline():

    def process_item(self, item, spider):
        pymysql.Connect(host='127.0.0.1', user='root', password='123456', port=3306,database='my_spider')

        return item


class ImagePipeline():

    def process_item(self, item, spider):
        if isinstance(item,U17ImagesItem):
            # TODO:item['chapter_name']文件名出错；超出索引；省略号结尾出错。使用正则筛选出中文
            name = item['name'].strip('. ')
            chapter_name = item['chapter_name'].strip(' .')
            path = 'u17漫画' + '/' + name + '/' + chapter_name
            if not os.path.exists(path):
                os.makedirs(path)
            urllib.request.urlretrieve(item['img_url'], path + '/' + item['page_num'] +'.jpg')
        return item