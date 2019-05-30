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