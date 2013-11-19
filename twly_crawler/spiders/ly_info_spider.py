# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from twly_crawler.items import TwlyCrawlerItem


urls_list = []
for id in range(1,117):
    urls_list.append("http://www.ly.gov.tw/03_leg/0301_main/legIntro.action?lgno=00%03d&stage=8" % (id))
class LyinfoSpider(BaseSpider):
    name = "ly_info"
    allowed_domains = ["ly.gov.tw"]
    start_urls = urls_list
    def parse(self, response):
        sel = Selector(response)
        items = []
        item = TwlyCrawlerItem()
        item['name'] = sel.xpath('//table/tr/td/ul/li/text()').re(u'^姓名：([\w]+)')
        item['gender'] = sel.xpath('//table/tr/td/ul/li/text()').re(u'^性別：([\w]+)')
        item['party'] = sel.xpath('//table/tr/td/ul/li/text()').re(u'^黨籍：([\w]+)')
        item['caucus'] = sel.xpath('//table/tr/td/ul/li/text()').re(u'^黨團：([\w]+)')
        item['constituency'] = sel.xpath('//table/tr/td/ul/li/text()').re(u'^選區：([\w]+)')
        item['committees'] = sel.xpath('//table/tr/td/ul/li/text()').re(u'^(第8屆第[\d]會期)：[\s]*([\w]+)')
        item['term_start'] = sel.xpath('//table/tr/td/ul/li/text()').re(u'到職日期：[\s]*([\d|/]+)')
        nodes = sel.xpath('//table/tr/td/ul[contains(@style, "list-style-position:outside;")]')
        item['contacts']=[]
        for node in nodes:
            if node.xpath('../span/text()').re(u'(電話|傳真)'):
                item['contacts'].append(node.xpath('div/text()').extract())
            elif node.xpath('../span/text()').re(u'學歷'):
                item['education'] = node.xpath('div/text()').extract()
            elif node.xpath('../span/text()').re(u'經歷'):
                item['experience'] = node.xpath('div/text()').extract()               
            elif node.xpath('../span/text()').re(u'通訊處'):
                item['contacts'].append(node.xpath('text()').re(u'[\s]*([\S]+)[\s]*'))
            elif node.xpath('../span/text()').re(u'備註'):
                item['term_end'] = node.xpath('font/text()').re(u'生效日期：[\s]*([\d|/]+)')
                item['term_end_reason'] = node.xpath('div/text()').extract()
                item['term_end_replacement'] = node.xpath('a/text()').extract()
        items.append(item)
        return items
