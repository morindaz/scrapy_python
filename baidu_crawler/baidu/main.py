#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime:2019-04-02 17:42
# software: PyCharm
# 将在cmd执行的语句放到pycharm中，需要引入scrapy.cmdline 执行的是spider的名字，名字在db.py-class DbSpider里面的name

from scrapy.cmdline import execute
execute('scrapy crawl bd'.split())