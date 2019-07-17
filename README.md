# DouBanScrapy
豆瓣TOP250爬虫项目

代码地址：

&emsp;&emsp;https://github.com/XieXiePro/DouBanScrapy

开发环境：

&emsp;&emsp;电脑系统：Win 10

&emsp;&emsp;IDE:PyCharm

&emsp;&emsp;Python第三方库：scrapy、pymysql、Flask

&emsp;&emsp;Python版本：Anaconda 3 ,集成Python版本 3.7

&emsp;&emsp;数据库： MySQL 8.0.12

### 第一步 创建scrapy项目

&emsp;&emsp;参考：[PyCharm创建scrapy项目](https://www.jianshu.com/p/d2c8b1496949)

### 第二步 使用Scrapy采集豆瓣TOP250数据

###### 1. 爬虫程序编写db.py
```
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from ..items import DoubanmovieItem
from urllib.parse import urljoin


class Douban(scrapy.spiders.Spider):
    name = "db"
    allowed_domains = ["douban.com"]
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        item = DoubanmovieItem()
        selector = Selector(response)
        movies = selector.xpath('//div[@class="item"]')
        for eachMovie in movies:
            rank = eachMovie.xpath('div[@class="pic"]/em/text()').extract()  # 排名
            img = eachMovie.xpath('div[@class="pic"]/a/img/@src').extract()  # 缩略图
            url = eachMovie.xpath('div/div[@class="hd"]/a/@href').extract()  # 详情地址
            title = eachMovie.xpath('div/div[@class="hd"]/a/span/text()').extract()  # 标题
            title = "".join(title)  # 将多个字符串无缝连接起来
            info = eachMovie.xpath('div/div[@class="bd"]/p/text()').extract()
            star = eachMovie.xpath('div/div[@class="bd"]/div[@class="star"]/span/text()').extract()
            count = eachMovie.xpath('div/div[@class="bd"]/div[@class="star"]/span/text()').extract()
            quote = eachMovie.xpath('div/div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            # quote可能为空，因此需要先进行判断
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['rank'] = rank
            item['img'] = img
            item['url'] = url
            item['title'] = title
            item['info'] = ';'.join(info).replace(' ', '').replace('\n', '')
            item['cost'] = item['info'].split(';')[0]
            item['info'] = item['info'].split(';')[1]
            item['star'] = star[0]
            item['count'] = count[1].split('人')[0]
            item['quote'] = quote
            print(rank)
            yield item
        nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        # 第10页是最后一页，没有下一页的链接
        if nextLink:
            nextLink = nextLink[0]
            yield Request(urljoin(response.url, nextLink), callback=self.parse)
```

###### 2. settings.py配置
```
# -*- coding: utf-8 -*-

BOT_NAME = 'db'

SPIDER_MODULES = ['db.spiders']
NEWSPIDER_MODULE = 'db.spiders'

#不遵循 robots.txt协议
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# 取消Cookies
COOKIES_ENABLED = False
# 重定向
REDIRECT_ENABLED = True
# 设置延迟下载可以避免被发现
DOWMLOAD_DELY = 5,

# 设置用户代理
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'

# 数据传输
ITEM_PIPELINES = {
    'db.pipelines.DbPipeline': 200,
}
```

##### 3.在items.py中添加存储容器对象
```
# -*- coding: utf-8 -*-
import scrapy

class DoubanmovieItem(scrapy.Item):
    rank = scrapy.Field()  # 电影排名
    img = scrapy.Field()  # 电影缩略图
    url = scrapy.Field()  # 电影详情链接
    title = scrapy.Field()  # 电影名字
    cost = scrapy.Field()  # 电影的描述信息，包括导演、主演等演职人员
    info = scrapy.Field()  # 电影类型等等
    star = scrapy.Field()  # 电影评分
    count = scrapy.Field()  # 参与评分人数
    quote = scrapy.Field()  # 电影中最经典或者说脍炙人口的一句话
    pass
```

### 第三步 将数据存储至MySQL数据库

&emsp;&emsp;1.在pipelines.py文件中写入数据库相关的代码

```
# -*- coding: utf-8 -*-
import pymysql
from twisted.enterprise import adbapi

class DbPipeline(object):
    # 链接数据库
    def __init__(self, ):
        dbparms = dict(
            host='localhost',
            db='estore',
            user='root',
            passwd='xp',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        # 指定擦做数据库的模块名和数据库参数参数
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

    # 使用twisted将mysql插入变成异步执行
    def process_item(self, item, spider):
        # 从item中导入
        rank = item['rank']
        img = item['img']
        url = item['url']
        title = item['title']
        cost = item['cost']
        info = item['info']
        star = item['star']
        count = item['count']
        quote = item['quote']

        import pandas as pd
        from sqlalchemy import create_engine
        # 数据框
        try:
            data = pd.DataFrame({"rank": rank, "title": title,
                                 "star": star, "count": count, "quote": quote,
                                 "img": img, "url": url, "info": info, "cost": cost}, index=[0])
            # print(data)

            # 将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
            connect = create_engine('mysql+pymysql://root:xieping@localhost:3306/estore?charset=utf8')
            pd.io.sql.to_sql(data, 'DB', connect, schema='estore', if_exists='append')
        except Exception as err:
            print('导入失败')
            print(err)
```

&emsp;&emsp;2.运行爬虫，在终端输入

```
scrapy crawl db
```

&emsp;&emsp;运行后结果：

![图片.png](https://upload-images.jianshu.io/upload_images/2783386-aba98bdbf2aeddca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 第四步 使用Flask读取MySQL数据库并展示数据

&emsp;&emsp;1.创建server.py
```
# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template, flash

import pymysql
import json
from bson import json_util

app = Flask(__name__)

def get_conn():
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="xp",
                           database="estore",)
    return conn

def toJson(data):
    return json.dumps(
               data,
               default=json_util.default,
               ensure_ascii=False
           )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def get_goods():
    if request.method == 'GET':
        conn = get_conn()
        cursor = conn.cursor()
        sql = "select * from DB"
        cursor.execute(sql)
        results = cursor.fetchall()

        resultList = []

        for result in results:
            resultList.append(result)

        return render_template('search.html', entries=resultList)

if __name__ == '__main__':
    app.run(debug=True)
```

&emsp;&emsp;2.创建html页面
```
{% extends "layout.html" %}
{% block body %}
<ul class="entries list-unstyled">
{% for entry in entries %}
  <li class="row">
    <div class="col-sm-2"></div>
    <div class="col-xs-2 col-sm-2">
      <span >排名：{{ entry[1] }}</span>
      <a href={{ entry[3] }} target="_blank">
        <img src="{{ entry[3] }}" alt="{{ entry[4] }}" width="100"><br/>
      </a>
    </div>
    <div class="col-xs-4 col-sm-4">
      <a href={{ entry[4] }} target="_blank">{{ entry[2] }}</a><br /><br />
      <span class="hidden-sm hidden-xs">导演：{{ entry[5] }}
        &nbsp;&nbsp;&nbsp; 题材：{{ entry[6] }}</span>
    </div>
    <div class="col-xs-3 col-sm-2">
      评分：{{ entry[7] }}<br/>
      <span class="hidden-sm hidden-xs">评论人数：{{ entry[8]}}</span><br/>
          <div class="col-xs-3 col-sm-2">
    </div>
      <span class="hidden-sm hidden-xs">{{ entry[9] }}</span>
    </div>
{% else %}
  <li><em>Unbelievable. No entries here so far.</em>
{% endfor %}
</ul>
{% endblock %}
```
&emsp;&emsp;使用浏览器访问 [http://127.0.0.1:5000/](http://127.0.0.1:5000/) ，运行后结果如下：

![图片.png](https://upload-images.jianshu.io/upload_images/2783386-54982e2f21e77c4c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)