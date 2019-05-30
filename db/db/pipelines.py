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
            passwd='xieping',
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