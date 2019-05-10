# 代码结构
### baidu_crawler
百度爬虫可执行的例子，data目录存放爬取好的文件，inputdata是需要爬取的文件名称

### baike_spider
爬取百度百科可执行的例子

### spider_learn
通过Urllib爬取网页的三种方式以及通过Beautifulsoup解析的方法

### website_crawler
scrapy框架，生成方法

1、pip install scrapy

2、scrapy startproject (projectname)

3、生成文件，进入projectname-spider

执行  scrapy genspider  (spidername) +域名

scrapy genspider douban_spider movie.douban.com



# Reference
1. [spider_learn代码，最基础的例子](https://www.runoob.com/w3cnote/python-spider-intro.html)
2. [baike_spider，配套百科爬取的例子,采用urllib](https://www.imooc.com/video/10677)
3. [spider_learn和baike_spider配套视频，采用urllib](https://www.imooc.com/video/10677)
4. [baidu_craweler, scrapy视频的配套例子，视频地址](https://www.imooc.com/video/17516)