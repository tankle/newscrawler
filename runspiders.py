# -*- coding: utf-8 -*-
# runspiders.py

import os
os.system('scrapy crawl tencent_news_spider &')
os.system('scrapy crawl netease_news_spider &')
os.system('scrapy crawl sina_news_spider &')
os.system('scrapy crawl sohu_news_spider &')
