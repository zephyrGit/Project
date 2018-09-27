# 1、Docker 安装

## 前提条件

目前，CentOS 仅发行版本中的内核支持 Docker。

Docker 运行在 CentOS 7 上，要求系统为64位、系统内核版本为 3.10 以上。

Docker 运行在 CentOS-6.5 或更高的版本的 CentOS 上，要求系统为64位、系统内核版本为 2.6.32-431 或者更高版本。

> ```
> 查看linux版本信息 uname -a
> ```

### 安装 Docker

从 2017 年 3 月开始 docker 在原来的基础上分为两个分支版本: Docker CE 和 Docker EE。

Docker CE 即社区免费版，Docker EE 即企业版，强调安全，但需付费使用。

本文介绍 Docker CE 的安装使用。

移除旧的版本：

```
$ sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```

安装一些必要的系统工具：

```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```

添加软件源信息：

```
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

更新 yum 缓存：

```
sudo yum makecache fast
```

使用yum安装docker，执行`yum -y install docker-io`，提示信息如下：

```
[root@host-10-200-143-61 ~]# yum -y install docker-io
Loaded plugins: fastestmirror
Setting up Install Process
Loading mirror speeds from cached hostfile
 * base: mirrors.cn99.com
 * extras: mirrors.163.com
 * updates: mirrors.163.com
No package docker-io available.
Error: Nothing to do123456789
```

# 排查原因

开始以为是没有升级yum导致安装失败的，而是执行`yum -y update` 成功后再次执行`yum -y install docker-io`，依然失败，按照上面执行命令`yum -y install epel-release`,然后在执行命令`yum -y install docker-io`，

## docker启动命令,docker重启命令,docker关闭命令

##### 启动        systemctl start docker

##### **-守护进程重启**   sudo systemctl daemon-reload

##### **重启docker服务**   systemctl restart  docker

##### **重启docker服务**  sudo service docker restart

##### 关闭docker service docker stop

##### 关闭docker systemctl stop docker

# 2、splash

目前，为了加速页面的加载速度，页面的很多部分都是用JS生成的，而对于用scrapy爬虫来说就是一个很大的问题，因为scrapy没有JS engine，所以爬取的都是静态页面，对于JS生成的动态页面都无法获得

**解决方案**

　　1、利用第三方中间件来提供JS渲染服务： [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash) 等。

　　2、利用selenium

　    Splash是一个Javascript渲染服务。它是一个实现了HTTP API的轻量级浏览器，Splash是用Python实现的，同时使用Twisted和QT。Twisted（QT）用来让服务具有异步处理能力，以发挥webkit的并发能力。



GitHub:https://github.com/scrapy-plugins/scrapy-splash

## docker 安装scrapy-splash

## scrapy settings 配置

## 新建请求

配置完成之后，我们就可以利用Splash来抓取页面了。我们可以直接生成一个`SplashRequest`对象并传递相应的参数，Scrapy会将此请求转发给Splash，Splash对页面进行渲染加载，然后再将渲染结果传递回来。此时Response的内容就是渲染完成的页面结果了，最后交给Spider解析即可。

```python
# request需要封装成SplashRequest
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                self.parse,
                                args={'wait': '0.5'}
                                )
```



# 完整代码

![img](jd.png)



## 1、settings.py

```python
# 连接scrapy-splash docker
SPLASH_URL = 'http://10.36.100.68:8050'

# 打开中splash中间件
SPIDER_MIDDLEWARES = {
    # 'jd.middlewares.JdSpiderMiddleware': 543,
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DOWNLOADER_MIDDLEWARES = {
    # 'jd.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# splash 去重
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# Cache存储
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```

## 2、items.py

```python
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

```

3、spiders.py

```python
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

```

4、结果

```json
{'buy_style': '官方标配',
 'color': '幻夜黑 海鸥灰 幻影蓝 幻影紫 铃兰白 ',
 'price': '￥2399.00',
 'promotion': '',
 'quality': '0.153kg',
 'staging': '不分期 ￥811.33起×3期 ￥411.64起×6期 ￥211.86起×12期 ￥111.83起×24期 ',
 'suit': '',
 'value_add': '高价回收-卖了换钱 3元1G ',
 'value_add_protection': '全保修2年 碎屏保1年 延长保1年 ',
 'version': '全网通（6GB 64GB） 全网通（6GB 128GB） 全网通（8GB 128GB） '}
```



