# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BigDataItem(scrapy.Item):
    company_id = scrapy.Field()
    company_name = scrapy.Field()
    industry_field = scrapy.Field()
    company_location = scrapy.Field()
    position_id = scrapy.Field()
    position_name = scrapy.Field()
    position_desc = scrapy.Field()
    salary = scrapy.Field()
