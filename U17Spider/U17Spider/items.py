# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class U17SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    img = scrapy.Field()
    chapters = scrapy.Field()


class U17ImagesItem(scrapy.Item):
    name = scrapy.Field()
    chapter_name = scrapy.Field()
    page_num = scrapy.Field()
    img_url = scrapy.Field()

