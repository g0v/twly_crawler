# -*- coding: utf-8 -*-
import re
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from twly_crawler.items import LegislatorItem


def take_first(list_in):
    if len(list_in) == 1:
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
        nodes = sel.xpath('//table/tr/td/a[contains(@href, "/do/www/commissionerInfo")]')
        for node in nodes:
            item = LegislatorItem()
            item['name'] = take_first(node.xpath('text()').re(u'[\s]*([\S]+)[\s]*'))
            match = re.search(u'id=(?P<id>[\d]*)&expireBack=0&expire=(?P<ad>[\d]*)', take_first(node.xpath('@href').extract()))
            if match:
                item['uid'] = int(match.group('id'))
                item['ad'] = int(match.group('ad'))
            else:
                raise Exception("id & ad not found!")
            if node.xpath('font/text()').re(u'離職'):
                item['in_office'] = False
            else:
                item['in_office'] = True 
            request = Request('http://%s%s' % (self.allowed_domains[0], take_first(node.xpath('@href').extract())), callback=self.parse_profile)
            request.meta['item'] = item
            yield request

    def parse_profile(self, response):
        sel = Selector(response)
        items = []
        item = response.request.meta['item']
        nodes = sel.xpath('//table/tr/td[@style="height:27"]')
        for node in nodes:
            if node.xpath('../td/font/text()').re(u'性別'):
                item['gender'] = take_first(node.xpath('text()').re(u'[\s]*([\S]+)[\s]*'))
            elif node.xpath('../td/font/text()').re(u'當選黨籍'):
                item['party'] = take_first(node.xpath('text()').re(u'[\s]*([\S]+)[\s]*'))
            elif node.xpath('../td/font/text()').re(u'選區'):
                item['constituency'] = take_first(node.xpath('text()').re(u'[\s]*([\S]+)[\s]*'))
            elif node.xpath('../td/font/text()').re(u'委員會'):
                item['committees'] = []
                committee_list = node.xpath('text()').re(u'第[\S]{1,2}屆第[\S]{1,2}會期[：|:][\s]*[\S]+[\s]*[\S]*')
                for committee in committee_list:
                    match = re.search(u'第(?P<ad>[\S]{1,2})屆第(?P<session>[\S]{1,2})會期[：|:][\s]*(?P<name>[\S]+)[\s]*(?P<chair>\(召委\))?', committee)
                    if match:
                        if match.group('chair'):
                            item['committees'].append({"session":'%02d%02d' % (int(match.group('ad')), int(match.group('session'))), "name":match.group('name'), "chair":True})
                        else:
                            item['committees'].append({"session":'%02d%02d' % (int(match.group('ad')), int(match.group('session'))), "name":match.group('name'), "chair":False})
            elif node.xpath('../td/font/text()').re(u'簡歷'):
                item['experience'] = node.xpath('text()').re(u'[\s]*([\S]+)[\s]*')
            elif node.xpath('../td/font/text()').re(u'備註'):
                item['remark'] = node.xpath('text()').re(u'[\s]*([\S]+)[\s]*')
        items.append(item)
        return items
