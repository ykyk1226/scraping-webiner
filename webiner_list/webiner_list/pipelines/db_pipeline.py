# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import pyodbc
import os

class DbPipeline:
    def open_spider(self, spider):
        version = '8.0'
        driver = 'FreeTDS'
        server = os.environ.get('ENV_DB_SERVER')
        port = os.environ.get('ENV_DB_PORT')
        database = os.environ.get('ENV_DATABASE')
        username = os.environ.get('ENV_USER')
        password = os.environ.get('ENV_PASSWORD')
        self.conn = pyodbc.connect('TDS_Version={%s};DRIVER={%s};SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' % (version, driver, server, port, database, username, password))

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        curs = self.conn.cursor()
        insert_flg = True

        # titleとurlが同一のwebinerはinsertしない
        select_sql = "SELECT title, url FROM webiner_lists WHERE title = ? and url = ?"
        curs.execute(select_sql, (item['title'], item['url']))
        res = curs.fetchall()
        for r in res:
            if r[0] == item['title'] and r[1] == item['url']:
                insert_flg = False
                break

        if insert_flg:
            insert_sql = "INSERT INTO webiner_lists VALUES (CAST(NEXT VALUE FOR WebinerListsSequence AS VARCHAR), ?, ?, ?, ?, ?, ?, ?)"
            curs.execute(insert_sql, (item['title'], item['url'], item['start_date'].strftime('%Y/%m/%d %H:%M:%S'), item['category_id'], spider.source_site_id, item['updated_at'], item['end_date'].strftime('%Y/%m/%d %H:%M:%S')))
            self.conn.commit()

        return item