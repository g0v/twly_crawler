# -*- coding: utf-8 -*-
import re
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from twly_crawler.items import LegislatorItem


def take_first(list_in):
    if len(list_in) == 1:
        return list_in[0]
    else:
        return list_in

class LyinfoSpider(BaseSpider):
    name = "ly_info"
    allowed_domains = ["www.ly.gov.tw"]
    urls_list = []
    ad = 8
    for id in range(1,117):
        urls_list.append("http://www.ly.gov.tw/03_leg/0301_main/legIntro.action?lgno=00%03d&stage=%d" % (id, ad))
    start_urls = urls_list
    def parse(self, response):
        sel = Selector(response)
        items = []
        item = LegislatorItem()
        item['ad'] = self.ad 
        item['name'] = take_first(sel.xpath('//table/tr/td/ul/li/text()').re(u'^姓名：([\S]+)'))
        item['gender'] = take_first(sel.xpath('//table/tr/td/ul/li/text()').re(u'^性別：([\S]+)'))
        item['party'] = take_first(sel.xpath('//table/tr/td/ul/li/text()').re(u'^黨籍：([\S]+)'))
        item['caucus'] = take_first(sel.xpath('//table/tr/td/ul/li/text()').re(u'^黨團：([\S]+)'))
        item['constituency'] = take_first(sel.xpath('//table/tr/td/ul/li/text()').re(u'^選區：([\S]+)'))
        item['term_start'] = take_first(sel.xpath('//table/tr/td/ul/li/text()').re(u'到職日期：[\s]*([\d|/]+)')).replace('/', '-')
        item['picture_url'] = 'http://www.ly.gov.tw' + take_first(sel.xpath('//table/tr/td/div/img[contains(@alt, ".jpg")]/@src').extract())
        item['committees'] = []
        committee_list = sel.xpath('//table/tr/td/ul/li/text()').re(u'^第[\d]屆第[\d]會期：[\s]*[\S]+[\s]*[\S]*')
        for committee in committee_list:
            match = re.search(u'第(?P<ad>\d)屆第(?P<session>\d)會期：[\s]*(?P<name>[\S]+)[\s]*(?P<chair>\(召集委員\))?', committee)
            if match:
                if match.group('chair'):
                    item['committees'].append({"session":'0%s0%s' % (match.group('ad'), match.group('session')), "name":match.group('name'), "chair":True})
                else:
                    item['committees'].append({"session":'0%s0%s' % (match.group('ad'), match.group('session')), "name":match.group('name'), "chair":False})
        nodes = sel.xpath('//table/tr/td/ul[contains(@style, "list-style-position:outside;")]')
        item['contacts'] = {}
        item['in_office'] = True
        for node in nodes:
            if node.xpath('../span/text()').re(u'電話'):
                item['contacts']['phone'] = take_first(node.xpath('div/text()').extract())
            elif node.xpath('../span/text()').re(u'傳真'):
                item['contacts']['fax'] = take_first(node.xpath('div/text()').extract())
            elif node.xpath('../span/text()').re(u'通訊處'):
                item['contacts']['address'] = take_first(node.xpath('text()').re(u'[\s]*([\S]+)[\s]*'))
            elif node.xpath('../span/text()').re(u'學歷'):
                item['education'] = take_first(node.xpath('div/text()').extract())
            elif node.xpath('../span/text()').re(u'經歷'):
                item['experience'] = take_first(node.xpath('div/text()').extract())               
            elif node.xpath('../span/text()').re(u'備註'):
                item['term_end'] = {}
                item['term_end']['date'] = take_first(node.xpath('font/text()').re(u'生效日期：[\s]*([\d|/]+)')).replace('/', '-')
                item['term_end']['reason'] = take_first(node.xpath('div/text()').extract())
                item['term_end']['replacement'] = take_first(node.xpath('a/text()').extract())
                item['in_office'] = False
        items.append(item)
        return items
