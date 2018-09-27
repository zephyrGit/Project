# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from jd.items import JdItem

class MyjdSpider(scrapy.Spider):
    name = 'myjd'
    allowed_domains = ['jd.com']
    start_urls = ['http://item.jd.com/7081550.html']

    # request需要封装成SplashRequest
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                self.parse,
                                args={'wait': '0.5'}
                                )

    def parse(self, response):

        # 如果想一直抓取可以使用CrawlSpider，或者把下面的注释去掉
        it_list = []
        it = JdItem()
        # 京东价
        prices = response.xpath('//span[@class="p-price"]/span/text()')
        it['price'] = prices[0].extract() + prices[1].extract()
        print('京东价：' + it['price'])

        # 促　销
        cxs = response.xpath('//div[@class="J-prom-phone-jjg"]/em/text()')
        strcx = ''
        for cx in cxs:
            strcx += str(cx.extract()) + ' '
        it['promotion'] = strcx
        print('促销:%s ' % strcx)

        # 增值业务
        value_addeds = response.xpath('//ul[@class="choose-support lh"]/li/a/span/text()')
        strValueAdd = ''
        for va in value_addeds:
            strValueAdd += str(va.extract()) + ' '
        print('增值业务:%s ' % strValueAdd)
        it['value_add'] = strValueAdd

        # 重量
        quality = response.xpath('//div[@id="summary-weight"]/div[2]/text()')
        print('重量:%s ' % str(quality[0].extract()))
        it['quality'] = quality[0].extract()

        # 选择颜色
        colors = response.xpath('//div[@id="choose-attr-1"]/div[2]/div/@title')
        strcolor = ''
        for color in colors:
            strcolor += str(color.extract()) + ' '
        print('选择颜色:%s ' % strcolor)
        it['color'] = strcolor

        # 选择版本
        versions = response.xpath('//div[@id="choose-attr-2"]/div[2]/div/@data-value')
        strversion = ''
        for ver in versions:
            strversion += str(ver.extract()) + ' '
        print('选择版本:%s ' % strversion)
        it['version'] = strversion

        # 购买方式
        buy_style = response.xpath('//div[@id="choose-type"]/div[2]/div/a/text()')
        print('购买方式:%s ' % str(buy_style[0].extract()))
        it['buy_style'] = buy_style[0].extract()

        # 套装
        suits = response.xpath('//div[@id="choose-suits"]/div[2]/div/a/text()')
        strsuit = ''
        for tz in suits:
            strsuit += str(tz.extract()) + ' '
        print('套装:%s ' % strsuit)
        it['suit'] = strsuit

        # 增值保障
        vaps = response.xpath('//div[@class="yb-item-cat"]/div[1]/span[1]/text()')
        strvaps = ''
        for vap in vaps:
            strvaps += str(vap.extract()) + ' '
        print('增值保障:%s ' % strvaps)
        it['value_add_protection'] = strvaps

        # 白条分期
        stagings = response.xpath('//div[@class="baitiao-list J-baitiao-list"]/div[@class="item"]/a/strong/text()')
        strstaging = ''
        for st in stagings:
            ststr = str(st.extract())
            strstaging += ststr.strip() + ' '
        print('白天分期:%s ' % strstaging)
        it['staging'] = strstaging

        it_list.append(it)
        return it_list
