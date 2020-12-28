# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import pyodbc

class DbPipeline:
    def open_spider(self, spider: scrapy.Spider):
        driver = 'ODBC Driver 17 for SQL Server'
        server = 'scraping-app-db.database.windows.net'
        username = 'appuser'
        password = 'P@ssword'
        self.conn = pyodbc.connect('DRIVER={%s};SERVER=%s;UID=%s;PWD=%s' % (driver, server, username, password))

    def close_spider(self, spider: scrapy.Spider):
        self.conn.close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        curs = self.conn.cursor()
        sql = "INSERT INTO webiner_lists VALUES (CAST(NEXT VALUE FOR WebinerListsSequence AS VARCHAR), %s, %s, %s)"
        curs.execute(sql, (item['title'], item['url'], item['date'].strftime('%Y/%m/%d %H:%M:%S')))
        self.conn.commit()

        return item