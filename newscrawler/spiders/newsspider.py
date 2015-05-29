
from newscrawler.items import NewsItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector

import re

def ListCombiner(lst):
    string = ''
    for e in lst:
        string += e
    return string

class NewsSpider(CrawlSpider):
    name = 'news_spider'
    allowed_domains = ['news.163.com', 'news.sina.com.cn', 'news.qq.com']
    start_urls = ['http://news.163.com','http://news.sina.com.cn', 'http://news.qq.com']

    url_pattern_163 = r'(http://news\.163\.com)/(\d{2})/(\d{4})/\d+/(\w+)\.html'
    url_pattern_sina = r'(http://(?:\w+\.)*news\.sina\.com\.cn)/.*/(\d{4}-\d{2}-\d{2})/\d{4}(\d{8})\.(?:s)html'
    url_pattern_qq = r'(.*)/a/(\d{8})/(\d+)\.htm'

    rules = [Rule(LxmlLinkExtractor(allow=[url_pattern_163]), 'parse_netease', follow=True)]
    rules.extend([Rule(LxmlLinkExtractor(allow=[url_pattern_sina]), 'parse_sina', follow=True)])
    rules.extend([Rule(LxmlLinkExtractor(allow=[url_pattern_qq]), 'parse_qq', follow=True)])
    
    def parse_news(self, response):
        url = str(response.url)

        if url.find("163.com"):
            item = self.parse_netease(response)
        elif url.find("qq.com"):
            item = self.parse_qq(response)
        elif url.find("sina.com"):
            item = self.parse_sina(response)

        return item

    def parse_netease(self, response):
        sel = Selector(response)
        pattern = re.match(self.url_pattern_163, str(response.url))
        
        item = NewsItem()
        item['source'] = "news.163.com" #pattern.group(1)
        item['date'] = '20' + pattern.group(2) + pattern.group(3)
        item['newsId'] = pattern.group(4)
        item['contents'] = {'link':str(response.url), 'title':u'', 'passage':u''}
        item['contents']['title'] = sel.xpath("//h1[@id='h1title']/text()").extract()[0]
        item['contents']['passage'] = ListCombiner(sel.xpath('//p/text()').extract())
        return item        

    def parse_sina(self, response):
        sel = Selector(response)
        pattern = re.match(self.url_pattern_sina, str(response.url))
        
        item = NewsItem()
        item['source'] = "news.sina.com.cn" #pattern.group(1)
        item['date'] = ListCombiner(str(pattern.group(2)).split('-'))
        item['newsId'] = sel.re(r'comment_id:(\d-\d-\d+)')[0]
        item['contents'] = {'link':str(response.url), 'title':u'', 'passage':u''}
        item['contents']['title'] = sel.xpath("//h1[@id='artibodyTitle']/text()").extract()[0]
        item['contents']['passage'] = ListCombiner(sel.xpath('//p/text()').extract())
        return item

    def parse_qq(self, response):
        sel = Selector(response)
        pattern = re.match(self.url_pattern_qq, str(response.url))

        item = NewsItem()
        item['source'] = "news.qq.com" #pattern.group(1)
        item['date'] = pattern.group(2)
        item['newsId'] = pattern.group(3)
        item['contents'] = {'link':str(response.url), 'title':u'', 'passage':u''}
        item['contents']['title'] = sel.xpath('//h1/text()').extract()[0]
        item['contents']['passage'] = ListCombiner(sel.xpath('//p/text()').extract())
        return item
