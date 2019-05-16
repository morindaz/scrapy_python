# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

#定义想要抓取
class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    type = Field()
    name = Field()
    con = Field()
    dosage = Field()
