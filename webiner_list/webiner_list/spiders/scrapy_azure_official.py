import scrapy
from webiner_list.items import AzureOfficialItem

class ScrapyAzureOfficialSpider(scrapy.Spider):
    name = 'scrapy_azure_official'
    allowed_domains = ['azure.microsoft.com']
    start_urls = ['https://azure.microsoft.com/ja-jp/community/events/?Page=1']

    def parse(self, response):
        # webiner一覧を取得
        for event in response.css('.row.event-item'):
            yield AzureOfficialItem(
                url = event.css('.column.medium-11 a::attr(href)').extract_first().strip(),
                title = event.css('.column.medium-11 a::text').extract_first().strip(),
                date = event.css('.column.medium-11 span::text').extract_first().strip()
            )
        # DB保存時に日本時間に直してから保存
        # datetime.datetime.strptime(date.split(" ", 1)[1].rsplit(" ", 1)[0],'%d %b %Y %H:%M:%S') + timedelta(hours=9)

        next_page_number = response.css('.row.column .wa-pagination li a::attr(data-pagination-page)')[-1].extract()
        if next_page_number == "2":
            next_page_link = response.css('.row.column .wa-pagination li a::attr(href)')[-1].extract()
            next_page_link = response.urljoin(next_page_link)
            yield scrapy.Request(next_page_link, callback=self.parse)

        return