# -*- coding: utf-8 -*-
import re
from urlparse import urljoin
import scrapy


def take_first(list_in):
    if len(list_in) == 1:
        return list_in[0]
    else:
        return list_in

def convert_contacts(dict_list):
    contacts_list = []
    for key, values in dict_list.items():
        for item in values:
            contact_dict, name_exist = {}, False
            match = re.search(u'(?P<name>[\S]+)[：:](?P<key>[\S]+)', item)
            if match:
                for place in contacts_list:
                    if place["name"] == match.group('name'):
                        place.update([(key, match.group('key'))])
                        name_exist = True
                if not name_exist:
                    contact_dict.update([("name", match.group('name')), (key, match.group('key'))])
                    contacts_list.append(contact_dict)
    return contacts_list

class Spider(scrapy.Spider):
    name = "ly_info"
    allowed_domains = ["www.ly.gov.tw"]
    #server has some anti-ddos protection and we need some delay to avoid fetch failure
    download_delay = 1

    def __init__(self, ad=None, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.ad = ad

    def start_requests(self):
        for ad in range(2, 10):
            if self.ad and self.ad != str(ad):
                continue
            else:
                payload = {
                    'queryFlag': 'true',
                    'searchValues[1]': str(ad),
                    'searchValues[5]': 'lgno',
                    'searchValues[6]': 'asc'
                }
                yield scrapy.FormRequest('http://www.ly.gov.tw/03_leg/0301_main/legList.action', formdata=payload, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for href in response.xpath('//*[@class="leg03_news_search_03"]/a/@href').extract():
            url = urljoin(response.url, href)
            yield scrapy.Request(url, callback=self.parse_profile)

    def parse_profile(self, response):
        """ get the following information
            { links        : {ly : },
              ad           :
              caucus       :
              constituency :
              committee    :
              education    :
              experience   : []
              gender       :
              name         :
              party        :
              term_start   :
              term_end     : { date :
                               reason :
                               replacement :
                             }
              contacts     : [{ name :
                               phone :
                               fax :
                               address :
                             }]
            }
        """

        item = {}
        item['links'] = {
            "ly": response.url
        }
        item['ad'] = int(re.search(u'stage=([\d]{1,2})', response.url).group(1))
        item['name'] = take_first(response.xpath('//table/tr/td/ul/li/text()').re(u'^姓名：([\S]+)'))
        item['gender'] = take_first(response.xpath('//table/tr/td/ul/li/text()').re(u'^性別：([\S]+)'))
        item['party'] = take_first(response.xpath('//table/tr/td/ul/li/text()').re(u'^黨籍：([\S]+)'))
        item['caucus'] = take_first(response.xpath('//table/tr/td/ul/li/text()').re(u'^黨\(政\)團：([\S]+)'))
        item['constituency'] = take_first(response.xpath('//table/tr/td/ul/li/text()').re(u'^選區：([\S]+)'))
        term_start = take_first(response.xpath('//table/tr/td/ul/li/text()').re(u'到職日期：[\s]*([\d|/]+)'))
        if term_start:
            item['term_start'] = term_start.replace('/', '-')
        item['image'] = 'http://www.ly.gov.tw%s' % (take_first(response.xpath('//table/tr/td/div/img[@class="leg03_pic"]/@src').extract()))
        item['committees'] = []
        committee_list = response.xpath('//table/tr/td/ul/li/text()').re(u'^第[\d]{1,2}屆第[\d]{1,2}會期：[\s]*[\S]+[\s]*[\S]*')
        for committee in committee_list:
            match = re.search(u'第(?P<ad>[\d]{1,2})屆第(?P<session>[\d]{1,2})會期：[\s]*(?P<name>[\S]+)[\s]*(?P<chair>\(召集委員\))?', committee)
            if match:
                if match.group('chair'):
                    item['committees'].append({"ad": int(match.group('ad')), "session": int(match.group('session')), "name":match.group('name'), "chair":True})
                else:
                    item['committees'].append({"ad": int(match.group('ad')), "session": int(match.group('session')), "name":match.group('name'), "chair":False})
        nodes = response.xpath('//table/tr/td/ul[contains(@style, "list-style-position:outside;")]')
        contacts = {}
        item['in_office'] = True
        for node in nodes:
            if node.xpath('../span/text()').re(u'電話'):
                contacts['phone'] = node.xpath('div/text()').extract()
            elif node.xpath('../span/text()').re(u'傳真'):
                contacts['fax'] = node.xpath('div/text()').extract()
            elif node.xpath('../span/text()').re(u'通訊處'):
                contacts['address'] = node.xpath('text()').re(u'[\s]*([\S]+)[\s]*')
            elif node.xpath('../span/text()').re(u'學歷'):
                item['education'] = node.xpath('div/text()').extract()
            elif node.xpath('../span/text()').re(u'經歷'):
                item['experience'] = node.xpath('div/text()').extract()
            elif node.xpath('../span/text()').re(u'備註'):
                item['term_end'] = {}
                term_end_date = take_first(node.xpath('font/text()').re(u'生效日期：[\s]*([\d|/]+)'))
                if term_end_date:
                    item['term_end']['date'] = term_end_date.replace('/', '-')
                else:
                    item['term_end']['date'] = None
                item['term_end']['reason'] = take_first(node.xpath('div/text()').extract())
                item['term_end']['replacement'] = take_first(node.xpath('a/text()').extract())
                item['in_office'] = False
        if contacts:
            item['contacts'] = convert_contacts(contacts)
        yield item
