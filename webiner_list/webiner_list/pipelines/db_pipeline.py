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
        driver = '/usr/local/lib/libtdsodbc.0.so'
        server = 'scraping-app-db.database.windows.net'
        port = "1433"
        database = "scraping-app-db"
        username = 'appuser'
        password = 'P@ssword'
        self.conn = pyodbc.connect('DRIVER={%s};SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' % (driver, server, port, database, username, password))

    def close_spider(self, spider: scrapy.Spider):
        self.conn.close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        curs = self.conn.cursor()
        delete_sel = "DELETE FROM webiner_lists"
        curs.execute(delete_sel)
        insert_sql = "INSERT INTO webiner_lists VALUES (CAST(NEXT VALUE FOR WebinerListsSequence AS VARCHAR), ?, ?, ?, ?)"
        curs.execute(insert_sql, (item['title'], item['url'], item['date'].strftime('%Y/%m/%d %H:%M:%S'), item['category_id']))
        self.conn.commit()

        return item