# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from pymongo import MongoClient
# class MongoPipeline(object):
#     def __init__(self,databaseIp = '127.0.0.1',databasePort = 27017, mongodbName='zhongan'):
#         client = MongoClient(databaseIp,databasePort)
#         self.db = client[mongodbName]


# class BaiduPipeline(object):
#     def process_item(self, item, spider):
#             if not os.path.exists('./data_1'):
#                 os.mkdir('./data_1')
#             # print("make dir successfully")
#             name = item['name']
#             con = item['con']
#             dosage = item['dosage']
#             print(item)
            # 将\进行转义
            # for ix in
            # with open('./data_1/' + name[0] + '.txt', 'a', encoding='utf-8') as f:
            #     f.write(dosage[0] + '\n')
            # return item
#             # postItem = dict(item)  # 把item转化成字典形式
#             # self.db.scrapy.insert(postItem)


class BaiduPipeline(object):
            def __init__(self, mongodbname='zhongan'):
                client = MongoClient('127.0.0.1', 27017)
                self.db = client[mongodbname]

            def process_item(self, item, spider):
                for index, item_child in enumerate(item['name']):
                    postItem={"type": item['type'], "name": item_child, "con": item['con'][index], "dosage": item['dosage'][index]}
                    self.db.scrapy.insert(postItem)


        #     def process_item(self, item, spider):
        #         # if not os.path.exists('./data'):
        #         #     os.mkdir('./data')
        #         name = item['name']
        #         text = item['text']
        #         # name = name.replace('/', '\\')  # 将\进行转义
        #         # with open('./data/' + name + '.txt', 'a', encoding='utf-8') as f:
        #     f.write(text + '\n')
        # return item
        # # 把item转化成字典形式
        #
        # self.db.name.insert(text)
