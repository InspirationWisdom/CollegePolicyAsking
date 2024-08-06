
# 项目的目标文件，用于定义需要爬取的数据字段，类似于Django的models.py文件

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 是可以定义多个类的，每个类对应一个爬虫
class ItcastItem(scrapy.Item):
    # 姓名
    name = scrapy.Field()
    # 职称
    title = scrapy.Field()
    # 个人简介
    info = scrapy.Field()

class SZCUItem(scrapy.Item):
    # 文章标题
    arti_title = scrapy.Field()
    # 文章链接
    arti_link = scrapy.Field()
    # 文章创建者
    arti_creator = scrapy.Field()
    # 文章发布时间
    arti_time = scrapy.Field()
    # 文章目录
    arti_catalog = scrapy.Field()
    # 文章单位
    arti_institution = scrapy.Field()
    # 文章正文
    arti_content = scrapy.Field()
    # 文章附件
    arti_file = scrapy.Field()
    # 文章附件链接
    arti_file_link = scrapy.Field()
    # 文章正文内部链接
    arti_content_link = scrapy.Field()
    #文章正文的图片链接
    arti_img_link = scrapy.Field()
    #浏览次数
    arti_views = scrapy.Field()

