# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import copy
import image
import sys

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy import signals
import xlsxwriter

from sportsbook.exporter.csv_item_exporter import WorldOfSweetsCsvItemExporter
reload(sys)
sys.setdefaultencoding('utf8')


class WorldOfSweetsImageDownloader(ImagesPipeline):
    # CONVERTED_ORIGINAL = re.compile('^/[0-9,a-f,_,-,/]+.jpg$')

    # name information coming from the spider, in each item
    # add this information to Requests() for individual images downloads
    # through "meta" dict
    def get_media_requests(self, item, info):
        return [Request(item.get('image_urls'), meta={'title': item["image"]})]

    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        for key, image, buf, in super(WorldOfSweetsImageDownloader, self).get_images(response, request, info):
            # if self.CONVERTED_ORIGINAL.match(key):
            key = self.change_filename(key, response)
            yield key, image, buf

    def change_filename(self, key, response):
        return response.meta['title']


class SportsbookXslxExportPipeline(object):
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
        self.workbook = xlsxwriter.Workbook('%s_products.xlsx' % spider.name)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.set_default_row(25)
        self.output_header()

    def output_header(self):
        # self.worksheet.write(self.row_count, 5, self.odds_company_title)
        # self.row_count += 1
        self.worksheet.write(self.row_count, 0, '轮次'.encode('utf-8'))
        self.worksheet.write(self.row_count, 1, '时间'.encode('utf-8'))
        self.worksheet.write(self.row_count, 2, '主隊'.encode('utf-8'))
        self.worksheet.write(self.row_count, 3, '比分'.encode('utf-8'))
        self.worksheet.write(self.row_count, 4, '客隊'.encode('utf-8'))
        self.worksheet.write(self.row_count, 5, '让球'.encode('utf-8'))
        self.row_count += 1

    def spider_closed(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        # print('item[%s] to be processed:' % (item['name']))
        # write 'host_team','score','guest_team','initial_odd','final_odd'
        self.worksheet.write(self.row_count, 0, item['season_round'])
        self.worksheet.write(self.row_count, 1, item['round_date'])
        self.worksheet.write(self.row_count, 2, item['host_team'])
        self.worksheet.write(self.row_count, 3, item['score'])
        self.worksheet.write(self.row_count, 4, item['guest_team'])
        self.worksheet.write(self.row_count, 5, item['asia_handicap'])
        self.row_count += 1
        return item
