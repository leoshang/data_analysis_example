# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import copy
import image
import sys

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy import signals
import xlsxwriter

from asianbookie.sportsbook.exporter.oddsexporter import OddsExporter
from asianbookie.sportsbook.spiders.sportsbook_config import SportsbookConfiguration

reload(sys)
sys.setdefaultencoding('utf8')


class TitanAsianOddsExportPipeline(object):
    def __init__(self):
        self.workbook = {}
        self.worksheet = {}
        self.row_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file_prefix = SportsbookConfiguration.get_bookiename() + '-' + \
                      SportsbookConfiguration.get_league() + '-' + SportsbookConfiguration.get_current_season()
        self.workbook = xlsxwriter.Workbook('%s.xlsx' % file_prefix)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.set_default_row(25)
        self.output_header()

    def output_header(self):
        self.worksheet.write(self.row_count, 0, '比赛Id'.encode('utf-8'))
        self.worksheet.write(self.row_count, 1, '初盘主队水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 2, '初盘盘口'.encode('utf-8'))
        self.worksheet.write(self.row_count, 3, '初盘客队水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 4, '即时主队水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 5, '即时盘口'.encode('utf-8'))
        self.worksheet.write(self.row_count, 6, '即时客队水位'.encode('utf-8'))
        self.row_count += 1

    def spider_closed(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        # print('item[%s] to be processed:' % (item['name']))
        if hasattr(item, 'schedule_id'):
            self.worksheet.write(self.row_count, 0, item['schedule_id'])
        if hasattr(item, 'asian_start_homewager'):
            self.worksheet.write(self.row_count, 1, item['asian_start_homewager'])
        if hasattr(item, 'asian_start_handicap'):
            self.worksheet.write(self.row_count, 2, item['asian_start_handicap'])
        if hasattr(item, 'asian_start_guestwager'):
            self.worksheet.write(self.row_count, 3, item['asian_start_guestwager'])
        if hasattr(item, 'asian_end_homewager'):
            self.worksheet.write(self.row_count, 4, item['asian_end_homewager'])
        if hasattr(item, 'asian_end_handicap'):
            self.worksheet.write(self.row_count, 5, item['asian_end_handicap'])
        if hasattr(item, 'asian_end_guestwager'):
            self.worksheet.write(self.row_count, 6, item['asian_end_guestwager'])
        self.row_count += 1
        return item
