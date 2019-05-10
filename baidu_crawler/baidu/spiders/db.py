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
    #
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
        urls_path = response.xpath("//div[@id='content_left']//h3")
        for url_path in urls_path:
            url_name = ''.join(url_path.xpath(".//text()").extract()).strip()
            url = url_path.xpath("./a/@href").extract_first()  # 未空的时候是广告 url
            name_search = self.search_pattern.search(url_name)
            if url and not name_search:
                if url_name not in self.names:
                    try:
                        yield Request(url=url, meta={'name': name}, callback=self.get_content)
                    except Exception as e:
                        self.num -= 1
                    self.num += 1
        if self.num < 10:
            next_url = response.xpath("//div[@id='page']/a[last()]/@href").extract_first()
            url = response.urljoin(next_url)
            yield Request(url=url, callback=self.get_url, meta={'name': name})
        else:
            self.num = 0

    def get_content(self, response):
        item = BaiduItem()
        name = response.meta.get('name')
        if 'baike.baidu.com' in response.url:
            text = list()
            content_list = response.xpath("//div[@class='content']//div[@class='para']")
            for content in content_list:
                content_text = content.xpath(".//text()").extract()
                text.append(''.join(content_text))
        else:
            article = goose.extract(raw_html=response.text)
            text = article.cleaned_text
        item['name'] = name
        item['text'] = ''.join(text)
        yield item
