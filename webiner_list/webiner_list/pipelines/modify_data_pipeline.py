# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime, timedelta
import scrapy

class ModifyDataPipeline:
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        # webiner開催時間を日本時間に修正
        if spider.name in ['scrapy_azure_official']:
            item['start_date'] = datetime.strptime(item['start_date'].split(" ", 1)[1].rsplit(" ", 1)[0],'%d %b %Y %H:%M:%S') + timedelta(hours=9)
            item['end_date'] = datetime.strptime(item['start_date'].split(" ", 1)[1].rsplit(" ", 1)[0],'%d %b %Y %H:%M:%S') + timedelta(hours=2)

        return item
