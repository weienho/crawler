# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CategoryItem(Item):
    collection = "categories"

    category_dir = Field()
    category = Field()

class BrandItem(Item):
    collection = "brands"

    brand_dir = Field()
    category = Field()
    brand = Field()


class GoodItem(Item):

    collection = 'goods'

    img_url = Field()
    product_id = Field()
    lr_brand_dir = Field()
    hr_brand_dir = Field()
    category = Field()
    brand = Field()