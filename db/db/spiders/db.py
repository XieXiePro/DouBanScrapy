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