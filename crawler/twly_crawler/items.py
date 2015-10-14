# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class LegislatorItem(Item):
    uid = Field()
    ad = Field()
    name = Field()
    former_names = Field()
    title = Field()
    gender = Field()
    elected_party = Field()
    party = Field()
    caucus = Field()
    constituency = Field()
    committees = Field()
    in_office = Field()
    term_start = Field()
    contacts = Field()
    term_end = Field()
    education = Field()
    experience = Field()
    image = Field()
    remark = Field()
    links = Field()
