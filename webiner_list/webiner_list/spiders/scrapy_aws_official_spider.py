import scrapy
from webiner_list.items import WebinerItem
from datetime import datetime, date, timedelta
import re

class ScrapyAwsOfficialSpider(scrapy.Spider):
    name = 'scrapy_aws_official'
    allowed_domains = ['aws.amazon.com']
    start_urls = ['https://aws.amazon.com/jp/about-aws/events/webinars/']
    source_site_id = "2"

    def parse(self, response):
        # webiner一覧を取得
        for event in response.css('#aws-page-content > main > div:nth-child(4) > div > div > div.lb-mbox.js-mbox > div.lb-grid.lb-row.lb-row-max-large.lb-snap > div > div.lb-border-left.lb-border-p.lb-box'):
            url = event.css('a::attr(href)').extract_first().strip()
            try:
                title = event.css('a::text').extract_first().strip().split("）", 1)[1]

                # Webiner開催時間を抽出
                event_date_str = event.css('a::text').extract_first().strip().split("（", 1)[0]
                event_time_str = re.split(' |-', event.css('div.lb-sticky-subnav-links div::text').extract_first().strip())
                end_time_str = event_time_str[3]
                start_time_str = event_time_str[2]
                # UTCでDBに登録するために調整
                end_date = datetime.strptime(str(date.today().year) + " " + event_date_str + " " + end_time_str,'%Y %m/%d %H:%M') - timedelta(hours=9)
                start_date = datetime.strptime(str(date.today().year) + " " + event_date_str + " " + start_time_str,'%Y %m/%d %H:%M') - timedelta(hours=9)
            except IndexError:
                continue

            yield WebinerItem(
                url = url,
                title = title,
                start_date = start_date,
                end_date = end_date,
                category_id = "2",
            )

        return