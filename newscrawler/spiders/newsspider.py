
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


class NeteaseNewsSpider(CrawlSpider):
    name = 'netease_news_spider'
    allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com']
    url_pattern = r'(http://news\.163\.com)/(\d{2})/(\d{4})/\d+/(\w+)\.html'
    rules = [Rule(LxmlLinkExtractor(allow=[url_pattern]), 'parse_news', follow=True)]
    
    def parse_news(self, response):
        sel = Selector(response)
        pattern = re.match(self.url_pattern, str(response.url))
        
        item = NewsItem()
        item['source'] = 'news.163.com' # pattern.group(1)
        item['date'] = '20' + pattern.group(2) + pattern.group(3)
        item['newsId'] = pattern.group(4)
        item['contents'] = {'link':str(response.url), 'title':u'', 'passage':u''}
        item['contents']['title'] = sel.xpath("//h1[@id='h1title']/text()").extract()[0]
        item['contents']['passage'] = ListCombiner(sel.xpath('//p/text()').extract())
        return item

class SinaNewsSpider(CrawlSpider):
    name = 'sina_news_spider'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn']
    url_pattern = r'(http://(?:\w+\.)*news\.sina\.com\.cn)/.*/(\d{4}-\d{2}-\d{2})/\d{4}(\d{8})\.(?:s)html'
    rules = [Rule(LxmlLinkExtractor(allow=[url_pattern]), 'parse_news', follow=True)]
    
    def parse_news(self, response):
        sel = Selector(response)
        pattern = re.match(self.url_pattern, str(response.url))
        
        item = NewsItem()
        item['source'] = 'news.sina.com.cn' # pattern.group(1)
        item['date'] = ListCombiner(str(pattern.group(2)).split('-'))
        item['newsId'] = sel.re(r'comment_id:(\d-\d-\d+)')[0]
        item['contents'] = {'link':str(response.url), 'title':u'', 'passage':u''}
        item['contents']['title'] = sel.xpath("//h1[@id='artibodyTitle']/text()").extract()[0]
        item['contents']['passage'] = ListCombiner(sel.xpath('//p/text()').extract())
        return item

class TencentNewsSpider(CrawlSpider):
    name = 'tencent_news_spider'
    allowed_domains = ['news.qq.com']
    start_urls = ['http://news.qq.com']
    url_pattern = r'(.*)/a/(\d{8})/(\d+)\.htm'
    rules = [Rule(LxmlLinkExtractor(allow=[url_pattern]), 'parse_news',follow=True)]
    
    def parse_news(self, response):
        sel = Selector(response)
        pattern = re.match(self.url_pattern, str(response.url))
        item = NewsItem()
        item['source'] = 'news.qq.com' # pattern.group(1)
        item['date'] = pattern.group(2)
        item['newsId'] = pattern.group(3)

        item['contents'] = {'link':str(response.url), 'title':u'', 'passage':u''}
        title = sel.xpath('//h1/text()').extract()
        if len(title) > 0:
            item['contents']['title'] = title[0]
        else:
            title = sel.xpath("//div[@id='ArticleTit']/text()").extract()
            item['contents']['title'] = title[0]
 
        item['contents']['passage'] = ListCombiner(sel.xpath('//p/text()').extract())
        return item

class NeteaseNewsSpider(CrawlSpider):
    name = 'sohu_news_spider'
    allowed_domains = ['sohu.com']
    start_urls = ['http://www.sohu.com']
    url_pattern = r'(http://.*?\.sohu\.com)/(\d{8})/(\w+)\.shtml'
    rules = [Rule(LxmlLinkExtractor(allow=[url_pattern]), 'parse_news', follow=True)]

    def parse_news(self, response):
        sel = Selector(response)
        pattern = re.match(self.url_pattern, str(response.url))

        item = NewsItem()
        item['source'] = 'www.sohu.com' # pattern.group(1)
        item['date'] = pattern.group(2)
        item['newsId'] = pattern.group(3)
        item['contents'] = {'link':str(response.url), 'title':u'', 'passage':u''}
        title = sel.xpath("//h1[@itemprop='headline']/text()").extract()
        if len(title) == 0:
            return None
        item['contents']['title'] = title[0]
        item['contents']['passage'] = ListCombiner(sel.xpath('//div[@id="contentText"]/p/text()').extract())
        return item

