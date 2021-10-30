# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# import pymongo
import os.path

import requests
import random
from pathlib import Path


class CategoryPipeline(object):
    def open_spider(self, spider):
        print("CategoryPipeline open_spider")
        self.lr_dir = spider.settings.get('LR_DIR')
        self.hr_dir = spider.settings.get('HR_DIR')

    def process_item(self, item, spider):

        # 创建商品分类目录
        lr_category_dir = os.path.join(self.lr_dir, item['category'])
        if not Path(lr_category_dir).exists():
            os.mkdir(lr_category_dir)

        hr_category_dir = os.path.join(self.hr_dir, item['category'])
        if not Path(hr_category_dir).exists():
            os.mkdir(hr_category_dir)
        return item


class BrandPipeline(object):
    def open_spider(self, spider):
        print("BrandPipeline open_spider")
        self.lr_dir = spider.settings.get('LR_DIR')
        self.hr_dir = spider.settings.get('HR_DIR')

    def process_item(self, item, spider):
        # 创建品牌目录
        lr_brand_dir = os.path.join(self.lr_dir, item['brand'])
        if not Path(lr_brand_dir).exists():
            os.mkdir(lr_brand_dir)

        hr_brand_dir = os.path.join(self.hr_dir, item['brand'])
        if not Path(hr_brand_dir).exists():
            os.mkdir(hr_brand_dir)
        return item


class GoodListPipeline(object):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     print("GoodListPipeline from_crawler")

    def open_spider(self, spider):
        print("GoodListPipeline open_spider")
        self.img_type = spider.settings.get('IMG_TYPE')
        self.lr_img_scale_suffix = spider.settings.get('LR_IMG_SCALE_SUFFIX')
        self.img_diff_size_list = spider.settings.get('IMG_DIFF_SIZE_LIST')


    def process_item(self, item, spider):
        print("GoodListPipeline process_item")

        brand = item["brand"]
        product_id = item["product_id"]
        lr_brand_dir = item["lr_brand_dir"]
        hr_brand_dir = item["hr_brand_dir"]
        img_url_parts = item["img_url"] .split("_")

        if len(img_url_parts) >= 3:
            img_diff_size_idx = random.randint(0, len(self.img_diff_size_list) - 1)

            img_url_parts[1] = self.img_diff_size_list[img_diff_size_idx]['lr']
            img_src_lr = "_".join(img_url_parts)

            lr_r = requests.get('https:' + img_src_lr, stream=True)
            with open(os.path.join(lr_brand_dir, brand + "_" + str(product_id) + self.lr_img_scale_suffix + self.img_type), 'wb') as lr_f:
                lr_f.write(lr_r.content)

            img_url_parts[1] = self.img_diff_size_list[img_diff_size_idx]['hr']
            img_src_hr = "_".join(img_url_parts)
            hr_r = requests.get('https:' + img_src_hr, stream=True)
            with open(os.path.join(hr_brand_dir, brand + "_" + str(product_id) + self.img_type), 'wb') as hr_f:
                hr_f.write(hr_r.content)

        return item

    def close_spider(self, spider):
        print("GoodListPipeline close_spider")


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        print("from_crawler")
        # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
    
    def open_spider(self, spider):
        print("open_spider")
        # self.client = pymongo.MongoClient(self.mongo_uri)
        # self.db = self.client[self.mongo_db]
    
    def process_item(self, item, spider):
        print("process_item")
        # self.db[item.collection].insert(dict(item))
        return item
    
    def close_spider(self, spider):
        print("close_spider")
        # self.client.close()