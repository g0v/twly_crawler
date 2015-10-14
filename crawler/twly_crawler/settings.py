# Scrapy settings for twly_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
import sys
from os.path import dirname


# add python path for crawler_lib
_PROJECT_PATH = dirname(dirname(dirname(__file__)))
sys.path.append(os.path.join(_PROJECT_PATH, 'crawler'))

BOT_NAME = 'twly_crawler'

SPIDER_MODULES = ['twly_crawler.spiders']
NEWSPIDER_MODULE = 'twly_crawler.spiders'
COOKIES_ENABLED = False
LOG_FILE = 'log.txt'
# for develop
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0

FEED_EXPORTERS = {
    'json': 'crawler_lib.misc.UnicodeJsonItemExporter',
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'twly_crawler (+http://www.yourdomain.com)'
