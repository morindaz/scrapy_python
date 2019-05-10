# -*- coding: utf-8 =*-
from baike_spider import url_manager
from baike_spider import html_downloader
from baike_spider import html_parser
from baike_spider import html_outputer


class SpiderMain(object):

    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOupter()

    def craw(self, root_utl):
        count = 1 #记录第几个url
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url(): #如果有待爬取的url
            try:
                new_url = self.urls.get_new_url() #取出url
                print('craw %d : %s' %(count, new_url))
                html_cont = self.downloader.download(new_url) #下载页面
                new_urls, new_data = self.parser.parse(new_url, html_cont) #解析页面
                self.urls.add_new_urls(new_urls) #将新的url补充进url管理器
                self.outputer.collect_data(new_data)
                if count == 100:
                    break
                count += 1
            except:
                print("craw failed %s" %new_url)

        self.outputer.output_html()

if __name__ == '__main__':
    root_url = "https://baike.baidu.com/item/Python/407313"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)