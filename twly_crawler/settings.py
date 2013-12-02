# Scrapy settings for twly_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'twly_crawler'

SPIDER_MODULES = ['twly_crawler.spiders']
NEWSPIDER_MODULE = 'twly_crawler.spiders'

#LOG_FILE = 'log.txt'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'twly_crawler (+http://www.yourdomain.com)'
