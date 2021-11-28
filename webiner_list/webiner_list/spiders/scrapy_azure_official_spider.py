import scrapy
from webiner_list.items import WebinerItem
from datetime import datetime, timedelta
import logging

class ScrapyAzureOfficialSpider(scrapy.Spider):
    name = 'scrapy_azure_official'
    allowed_domains = ['azure.microsoft.com']
    start_urls = ['https://events.microsoft.com/ja-jp/Azure']
    source_site_id = "1"

    def parse(self, response):
        logging.info("Start parsing in %s", self.start_urls)

        # webiner一覧を取得
        for event in response.css('.c-card.bgcolor-white'):
            try:
                url = event.css('.card-footer .c-button::attr(onclick)').extract_first().lstrip("window.open('").rstrip("', '_blank')")
                title = event.css('.gridcard-heading-favourite h3::text').extract_first().strip()
                event_date = event.css('.title-date::text').extract_first().strip()
                # PSTからJSTに変換（時間がPSTでない場合は例外をスロー）
                start_date = datetime.strptime(event_date.split(" - ", 1)[0],'%m/%d/%Y | %H:%M') + timedelta(hours=17)
                end_date = datetime.strptime(event_date.split("| ", 1)[0] + event_date.split("- ", 1)[1],'%m/%d/%Y %H:%M (PST)') + timedelta(hours=17)
            except ValueError as e:
                logging.error("Failed to parse in %s", self.start_urls)
                logging.error(e)
                continue

            yield WebinerItem(
                url = url,
                title = title,
                start_date = start_date,
                end_date = end_date,
                category_id = "1",
            )

        logging.info("Complete parsing in %s", self.start_urls)

        return