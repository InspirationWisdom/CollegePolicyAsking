
#项目的管道文件，用于处理数据，如存储到数据库，写入文件等

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MyspiderPipeline:
    def process_item(self, item, spider):
        return item
