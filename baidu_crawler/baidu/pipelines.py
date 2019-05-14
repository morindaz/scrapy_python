# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pymongo
from pymongo import MongoClient
# class BaiduPipeline(object):
#     def process_item(self, item, spider):
#         if not os.path.exists('./data1'):
#             os.mkdir('./data1')
#         name = item['name']
#         text = item['text']
#         name = name.replace('/', '\\')  # 将\进行转义
#         with open('./data1/' + name + '.txt', 'a', encoding='utf-8') as f:
#             f.write(text + '\n')
#         return item



class BaiduPipeline(object):
        def __init__(self, mongodbname='admin'):
            client = MongoClient('127.0.0.1', 27017)
            self.db = client[mongodbname]

        def process_item(self, item):
            postItem = dict(item)
            self.db.scrapy.insert(postItem)

            ## useless
            # word=[{"_id":1,"name":"sssss"}]
            # client = MongoClient('127.0.0.1',27017)
            # mongodbName="admin"
            # db = client[mongodbName]
            #
            # postItem = word
            # db.scrapy.insert(postItem)