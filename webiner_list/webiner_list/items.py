# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AzureOfficialItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    category_id = scrapy.Field()
    updated_at = scrapy.Field()
