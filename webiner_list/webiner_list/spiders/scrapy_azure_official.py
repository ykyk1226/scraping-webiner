import scrapy


class ScrapyAzureOfficialSpider(scrapy.Spider):
    name = 'scrapy_azure_official'
    allowed_domains = ['azure.microsoft.com']
    start_urls = ['http://azure.microsoft.com/ja-jp/community/events/?EventType=webinar']

    def parse(self, response):
        pass
