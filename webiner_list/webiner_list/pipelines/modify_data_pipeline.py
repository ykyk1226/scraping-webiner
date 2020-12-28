# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime, timedelta

class ModifyDataPipeline:
    def modify_date_to_jst(self, item, spider):
        if spider.name in ['scrapy_azure_official']:
            item['date'] = datetime.datetime.strptime(item['date'].split(" ", 1)[1].rsplit(" ", 1)[0],'%d %b %Y %H:%M:%S') + timedelta(hours=9)

        return item
