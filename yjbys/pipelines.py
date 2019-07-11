# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import datetime
import logging
import time

from scrapy.conf import settings


class YjbysPipeline(object):
    def open_spider(self, spider):
        self.now_timestamp = time.time()
        file_path = settings.get("FILE_PATH")
        self.file = open(file_path, 'a', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.file)
        headers = ['公司', '学校', '举办时间', '地点', '详情']
        self.csv_writer.writerow(headers)

    def process_item(self, item, spider):
        if '今天' in item['holding_time']:
            item['holding_time'] = item['holding_time'].replace('今天', self.get_today_time())
        elif '明天' in item['holding_time']:
            item['holding_time'] = item['holding_time'].replace('明天', self.get_next_day_time())
        else:
            item['holding_time'] = self.get_year() + item['holding_time']
        item['school'] = item['school'].replace('\n', '')
        holding_timestamp = item['holding_time'][0:10]
        strptime = time.strptime(holding_timestamp, "%Y-%m-%d")
        data_time = time.mktime(strptime)
        if data_time > self.now_timestamp:
            row = [item['company'], item['school'], item['holding_time'], item['addr'], item['href']]
            self.csv_writer.writerow(row)
            print(row)
            return item

    def close_spider(self, spider):
        try:
            self.file.closed()
        except Exception:
            logging.warning("\n\n======爬取完毕=====")

    def get_today_time(self):
        """
        当前日期 年月日
        """
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def get_next_day_time(self):
        """
        当前日期 年月日
        """
        return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    def get_year(self):
        """
            当前年
        """
        return time.strftime('%Y-', time.localtime(time.time()))
