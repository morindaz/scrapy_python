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
    search_pattern = re.compile(r'图片|百度文库|影像园')  # 不匹配的网站名称
    # 入口url,扔到调度器，调度器扔给引擎，高大上的引擎扔给下载器，下载器进行解析和下载
    start_url = 'https://www.baidu.com/s?&wd={text}&pn=0'
    num = 0
    names = tuple()

    def start_requests(self):
        file = pd.read_csv('./input_data/data.csv')
        names = tuple(file['name'][:10])
        for name in names:
            url = self.start_url.format(text=name, num=self.num)
            yield Request(url=url, callback=self.get_url, meta={'name': name})

    def get_url(self, response):
        name = response.meta.get('name')
        # 通过某个查询词获取一系列的关联文章
        urls_path = response.xpath("//div[@id='content_left']//h3")
        for url_path in urls_path:
            url_name = ''.join(url_path.xpath(".//text()").extract()).strip()
            url = url_path.xpath("./a/@href").extract_first()  # 未空的时候是广告 url
            name_search = self.search_pattern.search(url_name)
            if url and not name_search:
                if url_name not in self.names:
                    try:
                        # 通过每条文章网页的连接，调用get_content方法，提取网页内容，存储到item结构中
                        yield Request(url=url, meta={'name': name}, callback=self.get_content)
                    except Exception as e:
                        self.num -= 1
                    self.num += 1
        # 如果第一页的数据没有到10条，需要解析下一页的数据
        if self.num < 10:
            # 通过xpath提取下一页的url
            next_url = response.xpath("//div[@id='page']/a[last()]/@href").extract_first()
            url = response.urljoin(next_url)
            # 通过yield提交到调度器，回调函数写self.get_url
            yield Request(url=url, callback=self.get_url, meta={'name': name})
        else:
            self.num = 0

    # 进行解析，主要通过xpath插件对于网页内容进行分析
    def get_content(self, response):
        item = BaiduItem()
        name = response.meta.get('name')
        # 对于Baike数据单独处理
        if 'baike.baidu.com' in response.url:
            text = list()
            # 写xpath规则，提取出所需要的dom信息，现在存在在content_list（粗）里面
            content_list = response.xpath("//div[@class='content']//div[@class='para']")
            for content in content_list:
                # 对于xpath提取出比较粗的content_list信息进一步解析,也就是对于每个content(细)再采用一次xpath
                # 注意这里的xpath一定要加"." 表示在先前xpath语句的基础
                content_text = content.xpath(".//text()").extract()   # 然后调用extract()或者extract_first()
                text.append(''.join(content_text))
        else:
            article = goose.extract(raw_html=response.text)
            text = article.cleaned_text
        # 对于baiduitem的信息保存，保存的结构和在Item里面定义的字段保持一致
        item['name'] = name
        item['text'] = ''.join(text)
        # 将数据yield到pipeline里面
        yield item
