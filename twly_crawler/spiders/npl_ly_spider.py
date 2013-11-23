# -*- coding: utf-8 -*-
import re
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from twly_crawler.items import LegislatorItem


def take_first(list_in):
    if len(list_in) > 0:
        return list_in[0]
    else:
        return list_in

class npl_ly_Spider(BaseSpider):
    name = "npl_ly"
    allowed_domains = ["npl.ly.gov.tw"]
    start_urls = [
        "http://npl.ly.gov.tw/do/www/commissioner?orderBy=name&nameOrder=true&eleDisOrder=false&act=exp&expire=0&partyName=&keyword1=&keyword=&+%E6%9F%A5%E8%A9%A2+=+%E6%9F%A5%E8%A9%A2+",
    ]
    def parse(self, response):
        sel = Selector(response)
        items = []
        nodes = sel.xpath('//table/tr/td/a[contains(@href, "/do/www/commissionerInfo")]')
        for node in nodes:
            item = LegislatorItem()
            item["name"] = take_first(node.xpath('text()').extract()).strip()
            match = re.search(u'id=(?P<id>[\d]*)&expireBack=0&expire=(?P<ad>[\d]*)', take_first(node.xpath('@href').extract()))
            if match:
                item["id"] = int(match.group('id'))
                item["ad"] = int(match.group('ad'))
            if node.xpath('font/text()').re(u'離職'):
                item['in_office'] = False
            else:
                item['in_office'] = True 
            items.append(item)
        return items
