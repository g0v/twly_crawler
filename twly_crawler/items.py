# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TwlyCrawlerItem(Item):
    name = Field()
    gender = Field()
    party = Field()
    caucus = Field()
    constituency = Field()
    committees = Field()
    term_start = Field()
    contacts = Field()
    term_end = Field()
    term_end_reason = Field()
    term_end_replacement = Field()
    education = Field()
    experience = Field()
    pass
