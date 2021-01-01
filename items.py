# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonesItem(scrapy.Item):
    image_urls=scrapy.Field()
    images=scrapy.Field()
    name=scrapy.Field()
    clase=scrapy.Field()
    volumen_mL=scrapy.Field()
    price=scrapy.Field()
    links=scrapy.Field()
