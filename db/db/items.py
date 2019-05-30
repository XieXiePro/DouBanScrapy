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