# -*- coding: utf-8 -*-
import re
import urllib
from urllib.parse import urljoin
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from twly_crawler.items import LegislatorItem
from scrapy.utils.response import open_in_browser

class Spider(scrapy.Spider):
    name = "npl_ly"
    allowed_domains = ["lis.ly.gov.tw"]
    start_urls = [
        "https://lis.ly.gov.tw/lylegismc/lylegismemkmout?!!FUNC400",
    ]
    download_delay = 0.5

    def __init__(self, ad=None, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.ad = ad

    def parse(self, response):
        nodes = response.xpath('//ul[@id="ball_r"]//a')
        for node in nodes:
            if self.ad and self.ad != node.xpath('text()').extract_first():
                continue
            else:
                yield Request(urljoin(response.url, node.xpath('@href').extract_first()), callback=self.parse_ad, dont_filter=True)

    def parse_ad(self, response):
        open_in_browser(response)
        nodes = response.xpath('//div[@id="box01"]/table[@class="list01"]/tbody/tr/td/a[starts-with(@href, "/lylegisc")]')
        for node in nodes:
            href = node.xpath('@href').extract_first()
            yield Request(urljoin(response.url, href), callback=self.parse_profile, dont_filter=True)

    def parse_profile(self, response):
        item = LegislatorItem()
        item['ads'] = [int(x) for x in response.xpath('//*[@id="no"]/a/text()').extract()]
        item['in_office'] = True
        item['former_names'] = []
        nodes = response.xpath('//td[@class="info_bg"]/table/tr')
        for node in nodes:
            if node.xpath('td[1]/text()').re(u'^姓名$'):
                name_title = node.xpath('td[2]/text()').extract_first()
                m = re.search(u'\s*(\S*院長)', name_title)
                if not m:
                    item['name'] = name_title.strip()
                    item['title'] = u'立法委員'
                else:
                    item['name'] = re.sub(m.group(0), '', name_title)
                    item['title'] = m.group(1)
            elif node.xpath('td[1]/text()').re(u'^姓名參照$'):
                item['former_names'] = node.xpath('td[2]/text()').extract()
            elif node.xpath('td[1]/text()').re(u'^性別$'):
                item['gender'] = node.xpath('td[2]/text()').extract_first()
            elif node.xpath('td[1]/text()').re(u'^任期$'):
                item['ad'] = int(node.xpath('td[2]/text()').extract_first())
            elif node.xpath('td[1]/text()').re(u'^當選黨籍$'):
                item['elected_party'] = node.xpath('td[2]/text()').extract_first()
            elif node.xpath('td[1]/text()').re(u'^黨籍$'):
                item['party'] = node.xpath('td[2]/text()').extract_first()
            elif node.xpath('td[1]/text()').re(u'^選區$'):
                item['constituency'] = node.xpath('td[2]/text()').extract_first()
            elif node.xpath('td[1]/text()').re(u'^經歷$'):
                item['experience'] = node.xpath('td[2]//text()').re(u'[\s]*([\S]+)[\s]*')
            elif node.xpath('td[1]/text()').re(u'^離職日期$'):
                item['in_office'] = False
            elif node.xpath('td[1]/text()').re(u'^備註$'):
                item['remark'] = node.xpath('td[2]//text()').re(u'[\s]*([\S]+)[\s]*')
        yield item
