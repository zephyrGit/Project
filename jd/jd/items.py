# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 单价
    price = scrapy.Field()
    # description = Field()
    # 促销
    promotion = scrapy.Field()
    # 增值业务
    value_add = scrapy.Field()
    # 重量
    quality = scrapy.Field()
    # 选择颜色
    color = scrapy.Field()
    # 选择版本
    version = scrapy.Field()
    # 购买方式
    buy_style = scrapy.Field()
    # 套装
    suit = scrapy.Field()
    # 增值保障
    value_add_protection = scrapy.Field()
    # 白天分期
    staging = scrapy.Field()
