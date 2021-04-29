import scrapy
from webiner_list.items import AzureOfficialItem
import pytz
from datetime import datetime, timedelta
from urllib.request import urlopen
#from bs4 import BeautifulSoup

class ScrapyAzureOfficialSpider(scrapy.Spider):
    name = 'scrapy_azure_official'
    allowed_domains = ['azure.microsoft.com']
    start_urls = ['https://azure.microsoft.com/ja-jp/community/events/?Page=1']
    source_site_id = "1"

    # webiner詳細ページから終了時間を取得
    # def sub_parse(self, webiner_url):
    #     html = urlopen(webiner_url)
    #     data = html.read()
    #     html = data.decode('utf-8')
    #     soup = BeautifulSoup(html, "html.parser")
    #     print(html)
    #     iframe_src = soup.select_one("#myIframe").attrs["src"]
    #     iframe_html = urlopen(iframe_src)
    #     iframe_data = iframe_html.read()
    #     iframe_html = iframe_data.decode('utf-8')
    #     iframe_soup = BeautifulSoup(iframe_html, "html.parser")
    #     print(iframe_html)
    #     print(iframe_soup.find_all("span", class_="date"))
    #     return {
    #         'end_date' : soup.select('div#progDateTime.dateTime.mktoText'),
    #     }

    def parse(self, response):
        # webiner一覧を取得
        for event in response.css('.row.event-item'):
            webiner_url = event.css('.column.medium-11 a::attr(href)').extract_first().strip()
            #sub_response = self.sub_parse(webiner_url)

            # webiner開催時間を日本時間に修正
            end_date = event.css('.column.medium-11 span::text').extract_first().strip()
            start_date = event.css('.column.medium-11 span::text').extract_first().strip()
            end_date = datetime.strptime(start_date.split(" ", 1)[1].rsplit(" ", 1)[0],'%d %b %Y %H:%M:%S') + timedelta(hours=2)
            start_date = datetime.strptime(start_date.split(" ", 1)[1].rsplit(" ", 1)[0],'%d %b %Y %H:%M:%S')

            yield AzureOfficialItem(
                url = webiner_url,
                title = event.css('.column.medium-11 a::text').extract_first().strip(),
                start_date = start_date,
                end_date = end_date,
                category_id = "1",
                updated_at = datetime.now(pytz.timezone('Asia/Tokyo'))
            )

        next_page_number = response.css('.row.column .wa-pagination li a::attr(data-pagination-page)')[-1].extract()
        if next_page_number == "2":
            next_page_link = response.css('.row.column .wa-pagination li a::attr(href)')[-1].extract()
            next_page_link = response.urljoin(next_page_link)
            yield scrapy.Request(next_page_link, callback=self.parse)

        return