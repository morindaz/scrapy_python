# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


class BaiduPipeline(object):
    def process_item(self, item, spider):
        if not os.path.exists('./data'):
            os.mkdir('./data')
        name = item['name']
        text = item['text']
        name = name.replace('/', '\\')  # 将\进行转义
        with open('./data/' + name + '.txt', 'a', encoding='utf-8') as f:
            f.write(text + '\n')
        return item
