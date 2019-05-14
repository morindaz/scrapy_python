# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy import Request
import re
from goose3 import Goose
from goose3.text import StopWordsChinese
from ..items import BaiduItem

goose = Goose({'stopwords_class': StopWordsChinese,
               'browser_user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'})


class DbSpider(scrapy.Spider):
    # 这里是爬虫名字，和项目名称不能一致
    name = 'bd'
    # 允许的域名
    allowed_domains = list()

    # 入口url,扔到调度器，调度器扔给引擎，高大上的引擎扔给下载器，下载器进行解析和下载
    start_url = 'https://ypk.99.com.cn/'



    def start_requests(self):

        yield Request(url=self.start_url, callback=self.get_url)
        # yield Request(url=self.start_url, callback=self.get_content)


    def get_url(self,response):

        urls_path = response.xpath("//div[@class='sort_one']/a/@href").extract()
        urls_path =['https://ypk.99.com.cn'+urls for urls in urls_path]
        new_url = urls_path[-1]
        yield Request(url=new_url, callback=self.get_content)



        # urls_path = response.xpath("//div[@class='page']/a/@href").extract()
        # urls_path = ['https://ypk.99.com.cn'+urls for urls in set(urls_path)]
        #
        # url = url.urljoin(urls_path)
        # yield Request(url=url, callback=self.get_url)
        # yield Request(url=url, callback=self.get_content)



    # 进行解析，主要通过xpath插件对于网页内容进行分析
    def get_content(self, response):
        item = BaiduItem()
        # print(response.xpath("//p[@class='yp_tit cc']/a/@title").extract())
        item['name'] = response.xpath("//p[@class='yp_tit cc']/a/@title").extract()
        item['con'] = response.xpath("//p[@class='yp_con']/@title").extract()
        item['dosage'] = response.xpath("//p[@class='yp_dosage']/@title").extract()
        yield item
        try:
            next_url = response.xpath("//a[@class='page-next']/@href").extract()[0]
            next_url = 'https://ypk.99.com.cn'+next_url
            yield Request(url=next_url, callback=self.get_content)
        except:
            pass


   

