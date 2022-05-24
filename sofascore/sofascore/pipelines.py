# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import copy
import image
import sys

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy import signals
import xlsxwriter

from sofascore.spiders.sofa_config import SofaScoreConfiguration

reload(sys)
sys.setdefaultencoding('utf8')


class SofascorePipeline:
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
        league_season = 'SofaScore-' + SofaScoreConfiguration.get_league_name() + \
                        '-' + SofaScoreConfiguration.get_current_season()
        self.workbook = xlsxwriter.Workbook('%s_votes.xlsx' % league_season)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.set_default_row(25)
        self.output_header()

    def output_header(self):
        # self.worksheet.write(self.row_count, 5, self.odds_company_title)
        self.worksheet.write(self.row_count, 0, '本轮'.encode('utf-8'))
        self.worksheet.write(self.row_count, 1, '比赛ID'.encode('utf-8'))
        self.worksheet.write(self.row_count, 2, '比赛时间'.encode('utf-8'))
        self.worksheet.write(self.row_count, 3, '主队'.encode('utf-8'))
        self.worksheet.write(self.row_count, 4, '客队'.encode('utf-8'))
        self.worksheet.write(self.row_count, 5, '主队比分'.encode('utf-8'))
        self.worksheet.write(self.row_count, 6, '客队比分'.encode('utf-8'))
        self.worksheet.write(self.row_count, 7, '支持主赢人数'.encode('utf-8'))
        self.worksheet.write(self.row_count, 8, '支持平局人数'.encode('utf-8'))
        self.worksheet.write(self.row_count, 9, '支持客赢人数'.encode('utf-8'))
        self.worksheet.write(self.row_count, 10, '主队球迷数'.encode('utf-8'))
        self.worksheet.write(self.row_count, 11, '客队球迷数'.encode('utf-8'))
        self.row_count += 1

    def spider_closed(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        # print('item[%s] to be processed:' % (item['name']))
        if hasattr(item, 'round'):
            self.worksheet.write(self.row_count, 0, item['round'])
        if hasattr(item, 'match_id'):
            self.worksheet.write(self.row_count, 1, item['match_id'])
        if hasattr(item, 'startTimestamp'):
            self.worksheet.write(self.row_count, 2, item['startTimestamp'])

        if hasattr(item, 'hometeam'):
            self.worksheet.write(self.row_count, 3, item['hometeam'])
        if hasattr(item, 'guestteam'):
            self.worksheet.write(self.row_count, 4, item['guestteam'])

        if hasattr(item, 'hometeam_score'):
            self.worksheet.write(self.row_count, 5, item['hometeam_score'])
        if hasattr(item, 'guestteam_score'):
            self.worksheet.write(self.row_count, 6, item['guestteam_score'])

        if hasattr(item, 'vote_home_win'):
            self.worksheet.write(self.row_count, 7, item['vote_home_win'])
        if hasattr(item, 'vote_draw'):
            self.worksheet.write(self.row_count, 8, item['vote_draw'])
        if hasattr(item, 'vote_guest_win'):
            self.worksheet.write(self.row_count, 9, item['vote_guest_win'])

        if hasattr(item, 'hometeam_fans'):
            self.worksheet.write(self.row_count, 10, item['hometeam_fans'])
        if hasattr(item, 'guestteam_fans'):
            self.worksheet.write(self.row_count, 11, item['guestteam_fans'])
        self.row_count += 1
        return item
