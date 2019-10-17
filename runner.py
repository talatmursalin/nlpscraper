#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# author : mursalin
# date   : 2019-10-18

from scrapy.crawler import CrawlerProcess
import prothom_alo


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_LEVEL': 'ERROR'
})

process.crawl(prothom_alo.ProthomAlo)
try:
    process.start()
except KeyboardInterrupt as e:
    pass
