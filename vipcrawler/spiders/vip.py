# -*- coding: utf-8 -*-
import os
from pathlib import Path

from scrapy import Request, Spider
from vipcrawler.items import GoodItem
from scrapy.cmdline import execute


class VipSpider(Spider):
    name = 'vip'
    allowed_domains = ['www.vip.com', 'list.vip.com']
    base_url = "https://www.vip.com/"

    # base_url = 'https://detail.vip.com/detail-1710614625-6918479307584500993.html'
    # start_urls = ['https://www.vip.com/']

    def start_requests(self):
        # 请求商品分类列表
        yield Request(url=self.base_url, callback=self.category_parse, meta={}, dont_filter=True)

    def category_parse(self, response):
        category_a_tag_list = response.xpath('//ul[@id="J_main_nav_link"]//a[contains(@href,"//www.vip.com/nav")]')

        for tag_item in category_a_tag_list:
            category_href = ''
            hrefs = tag_item.xpath('./@href').extract()
            if len(hrefs) > 0:
                category_href = "https:" + hrefs[0]

            category_name = tag_item.xpath('.//text()').extract_first().strip()

            # 创建商品分配目录
            lr_category_dir = os.path.join(self.settings.get('LR_DIR'), category_name)
            if not Path(lr_category_dir).exists():
                os.makedirs(lr_category_dir)

            hr_category_dir = os.path.join(self.settings.get('HR_DIR'), category_name)
            if not Path(hr_category_dir).exists():
                os.makedirs(hr_category_dir)

            # 请求品牌列表
            yield Request(url= category_href, callback=self.brand_parse,
                          meta={
                              "lr_category_dir": lr_category_dir,
                              "hr_category_dir": hr_category_dir,
                                }, dont_filter=True)

    def brand_parse(self, response):
        lr_img_scale_suffix = self.settings.get('LR_IMG_SCALE_SUFFIX')

        lr_category_dir = response.request.meta.get('lr_category_dir', '')
        hr_category_dir = response.request.meta.get('hr_category_dir', '')
        brand_a_tag_list = response.xpath('//div[@id="J-index-channelb-brandlist"]//a[@class="brand-item-hover"]')

        for tag_item in brand_a_tag_list:
            brand_href = ''
            hrefs = tag_item.xpath('./@href').extract()
            if len(hrefs) > 0:
                brand_href = "https:" + hrefs[0]


            mars_exposure_modules = tag_item.xpath('./@mars_exposure_module').extract()
            brand = ''
            if len(mars_exposure_modules) > 0:
                 brand = mars_exposure_modules[0].split('|')[2]

            # 创建品牌目录
            lr_brand_dir = os.path.join(lr_category_dir,  brand, lr_img_scale_suffix)
            if not Path(lr_brand_dir).exists():
                os.makedirs(lr_brand_dir)

            hr_brand_dir = os.path.join(hr_category_dir, brand)
            if not Path(hr_brand_dir).exists():
                os.makedirs(hr_brand_dir)

            yield Request(url=brand_href, callback=self.good_parse, meta={'page': 1,
                                                                          "lr_brand_dir": lr_brand_dir,
                                                                          "hr_brand_dir": hr_brand_dir,
                                                                          'brand': brand,
                                                                          }, dont_filter=True)


    # 递归爬取同一页面的分页数据
    def good_parse(self, response):
        current_page = response.request.meta.get('page', 1)
        current_brand = response.request.meta.get('brand', 'brand')
        lr_brand_dir = response.request.meta.get('lr_brand_dir', '')
        hr_brand_dir = response.request.meta.get('hr_brand_dir', '')

        # 获取总页数
        total_page_text = response.xpath('//span[@class="total-item-nums"]//text()').extract_first()
        total_page = int(total_page_text[1:][:-1])

        good_list = response.xpath('//div[@class="c-goods-list"]//div[@id="J_wrap_pro_add"]//div[@class="c-goods-item  J-goods-item c-goods-item--auto-width"]')

        for good_item in good_list:
            product_id = good_item.xpath(".//@data-product-id").extract_first()
            # 图片使用延迟加载，可见：class="J-goods-item__img"，滚动可见的默认图：class="lazy J-goods-item__img"
            img_src = good_item.xpath('.//img[contains(@class,"J-goods-item__img")]/@src').extract_first()

            good_item = GoodItem()
            good_item["img_url"] = img_src
            good_item["product_id"] = product_id
            good_item["brand"] = current_brand
            good_item["lr_brand_dir"] = lr_brand_dir
            good_item["hr_brand_dir"] = hr_brand_dir
            yield good_item

        if current_page < total_page:
            next_page = current_page + 1
            yield Request(url=response.request.url, callback=self.good_parse, meta={'page': next_page,
                                                                                    "lr_brand_dir": lr_brand_dir,
                                                                                    "hr_brand_dir": hr_brand_dir,
                                                                                    'brand': current_brand,
                                                                                    'total_page': total_page}, dont_filter=True)

        # for product in products:
        #     item = ProductItem()
        #     item['image'] = ''.join(product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract()).strip()
        #     item['deal'] = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
        #     item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
        #     yield item


if __name__ == '__main__':
    execute(['scarpy', 'crawl', 'vip'])
