# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import mysql.connector
from mysql.connector import Error
from scrapy.exceptions import DropItem
from scrapy.http import Request
import json
import codecs

class SpiegelPipeline(object):

    table = 'news_data'
    conf = {
        'host': 'devvartpoddar.com',
        'user': 'server',
        'password': 'mysql@server',
        'database': 'de_elections',
        'raise_on_warnings': True
    }

    def __init__(self, **kwargs):
        self.cnx = self.mysql_connect()

    def open_spider(self, spider):
        print("The spider is now open!")

    def process_item(self, item, spider):
        self.save(dict(item))
        return item

    def close_spider(self, spider):
        self.mysql_close()

    def mysql_connect(self):
        try:
            return mysql.connector.connect(**self.conf)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def save(self, row):
        cursor = self.cnx.cursor()
        create_query = ("INSERT INTO " + self.table +
            "(url, date, text) "
            "VALUES (%(url)s, %(date)s, %(text)s)")

        # Insert new row
        cursor.execute(create_query, row)

        # Make sure data is committed to the database
        self.cnx.commit()
        cursor.close()

    def mysql_close(self):
        self.cnx.close()


class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('news.json', mode = 'wb', encoding = 'utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.encode().decode('unicode_escape'))
        return item
