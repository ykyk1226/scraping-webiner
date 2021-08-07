# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import pyodbc
import os
import pytz
from datetime import datetime

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

        curs = self.conn.cursor()

        # DBの要領削減のため実施済みのWebiner情報は削除する
        delete_sql = "DELETE FROM webiner_lists WHERE start_date < GETDATE()"
        curs.execute(delete_sql)

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        curs = self.conn.cursor()
        insert_flg = True
        updated_at = datetime.now(pytz.timezone('Asia/Tokyo'))

        # 既に登録済みのWebinerは登録しない
        select_sql = "SELECT title, url FROM webiner_lists WHERE title = ? and url = ?"
        curs.execute(select_sql, (item['title'], item['url']))
        rows = curs.fetchall()
        for row in rows:
            if row[0] == item['title'] and row[1] == item['url']:
                insert_flg = False
                break

        if insert_flg:
            insert_sql = "INSERT INTO webiner_lists VALUES (CAST(NEXT VALUE FOR WebinerListsSequence AS VARCHAR), ?, ?, ?, ?, ?, ?, ?)"
            curs.execute(insert_sql, (item['title'], item['url'], item['category_id'], spider.source_site_id, item['start_date'], item['end_date'], updated_at))

        return item