# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FashioncrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZalandoItem(scrapy.Item):

    title = scrapy.Field()
    price = scrapy.Field()
    remote_id = scrapy.Field()
    main_image = scrapy.Field()
    category = scrapy.Field()
    availability = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    extra_images = scrapy.Field()
    color = scrapy.Field()
    product_condition = scrapy.Field()
    variations = scrapy.Field()
    currency = scrapy.Field()


class ZalandoArticle(scrapy.Item):
    sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    image_url = scrapy.Field()
    article_url = scrapy.Field()


    def export(self):
        print('')
        print('_______Article___________')
        print(self['sku'])
        print(self['name'])
        print(self['brand'])
        print(self['color'])
        print(self['category'])
        print(self['price'])
        print(self['article_url'])
        print(self['image_url'])

        print('_________________________')
        print('')

