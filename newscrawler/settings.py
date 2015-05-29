# -*- coding: utf-8 -*-

# Scrapy settings for newscrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'newscrawler'

SPIDER_MODULES = ['newscrawler.spiders']
NEWSPIDER_MODULE = 'newscrawler.spiders'


ITEM_PIPELINES = {
        'newscrawler.pipelines.NewscrawlerPipeline': 1,
        }


DOWNLOAD_DELAY = 5

LOG_FILE = "news.crawl.log"

COOKIES_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'newscrawler (+http://www.yourdomain.com)'
