import scrapy
from webiner_list.items import WebinerItem
from datetime import datetime, timedelta

class ScrapyAzureOfficialSpider(scrapy.Spider):
    name = 'scrapy_azure_official'
    allowed_domains = ['azure.microsoft.com']
    start_urls = ['https://azure.microsoft.com/ja-jp/community/events/?Page=1']
    source_site_id = "1"

    def parse(self, response):
        # webiner一覧を取得
        for event in response.css('.row.event-item'):
            url = event.css('.column.medium-11 a::attr(href)').extract_first().strip()
            title = event.css('.column.medium-11 a::text').extract_first().strip()

            # webiner開催時間を日本時間に修正
            end_date = event.css('.column.medium-11 span::text').extract_first().strip()
            start_date = event.css('.column.medium-11 span::text').extract_first().strip()
            end_date = datetime.strptime(start_date.split(" ", 1)[1].rsplit(" ", 1)[0],'%d %b %Y %H:%M:%S') + timedelta(hours=2)
            start_date = datetime.strptime(start_date.split(" ", 1)[1].rsplit(" ", 1)[0],'%d %b %Y %H:%M:%S')

            yield WebinerItem(
                url = url,
                title = title,
                start_date = start_date,
                end_date = end_date,
                category_id = "1",
            )

        next_page_number = response.css('.row.column .wa-pagination li a::attr(data-pagination-page)')[-1].extract()
        if next_page_number == "2":
            next_page_link = response.css('.row.column .wa-pagination li a::attr(href)')[-1].extract()
            next_page_link = response.urljoin(next_page_link)
            yield scrapy.Request(next_page_link, callback=self.parse)

        return