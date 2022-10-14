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

from sportsbook.exporter.oddsexporter import OddsExporter
from sportsbook.spiders.sportsbook_config import SportsbookConfiguration

reload(sys)
sys.setdefaultencoding('utf8')


# class WorldOfSweetsImageDownloader(ImagesPipeline):
    #CONVERTED_ORIGINAL = re.compile('^/[0-9,a-f,_,-,/]+.jpg$')
    # name information coming from the spider, in each item
    # add this information to Requests() for individual images downloads
    # through "meta" dict

    #def get_media_requests(self, item, info):
    #    return [Request(item.get('image_urls'), meta={'title': item["image"]})]

    # this is where the image is extracted from the HTTP response
    # def get_images(self, response, request, info):
    #    for key, image, buf, in super(WorldOfSweetsImageDownloader, self).get_images(response, request, info):
            # if self.CONVERTED_ORIGINAL.match(key):
    #        key = self.change_filename(key, response)
    #        yield key, image, buf

    # def change_filename(self, key, response):
    #    return response.meta['title']


class Win007XslxExportPipeline(object):
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
        file_prefix = SportsbookConfiguration.get_league() + '-' + SportsbookConfiguration.get_current_season() \
                      + '-round' + SportsbookConfiguration.get_round_range()
        self.workbook = xlsxwriter.Workbook('%s.xlsx' % file_prefix)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.set_default_row(25)
        self.output_header()

    def output_header(self):
        self.worksheet.write(self.row_count, 0, '赛季'.encode('utf-8'))
        self.worksheet.write(self.row_count, 1, '轮次'.encode('utf-8'))
        self.worksheet.write(self.row_count, 2, '比赛时间'.encode('utf-8'))
        self.worksheet.write(self.row_count, 3, '比赛Id'.encode('utf-8'))

        self.worksheet.write(self.row_count, 4, '主队'.encode('utf-8'))
        self.worksheet.write(self.row_count, 5, '客队'.encode('utf-8'))

        self.worksheet.write(self.row_count, 6, '主队积分'.encode('utf-8'))
        self.worksheet.write(self.row_count, 7, '客队积分'.encode('utf-8'))

        self.worksheet.write(self.row_count, 8, '主队排名'.encode('utf-8'))
        self.worksheet.write(self.row_count, 9, '客队排名'.encode('utf-8'))

        self.worksheet.write(self.row_count, 10, '主队胜率'.encode('utf-8'))
        self.worksheet.write(self.row_count, 11, '客队胜率'.encode('utf-8'))
        # leave 12th. column empty
        self.worksheet.write(self.row_count, 13, '主队近6赢'.encode('utf-8'))
        self.worksheet.write(self.row_count, 14, '主队近6平'.encode('utf-8'))
        self.worksheet.write(self.row_count, 15, '主队近6负'.encode('utf-8'))
        # leave 16th. column empty
        self.worksheet.write(self.row_count, 17, '客队近6赢'.encode('utf-8'))
        self.worksheet.write(self.row_count, 18, '客队近6平'.encode('utf-8'))
        self.worksheet.write(self.row_count, 19, '客队近6负'.encode('utf-8'))

        self.worksheet.write(self.row_count, 20, '博彩公司'.encode('utf-8'))
        self.worksheet.write(self.row_count, 21, '初盘主胜赔付'.encode('utf-8'))
        self.worksheet.write(self.row_count, 22, '初盘平局赔付'.encode('utf-8'))
        self.worksheet.write(self.row_count, 23, '初盘客胜赔付'.encode('utf-8'))
        self.worksheet.write(self.row_count, 24, '初盘主队水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 25, '初盘盘口'.encode('utf-8'))
        self.worksheet.write(self.row_count, 26, '初盘客队水位'.encode('utf-8'))
        # leave 27th. column empty
        self.worksheet.write(self.row_count, 28, '即时终盘主胜赔付'.encode('utf-8'))
        self.worksheet.write(self.row_count, 29, '即时终盘平局赔付'.encode('utf-8'))
        self.worksheet.write(self.row_count, 30, '即时终盘客胜赔付'.encode('utf-8'))
        self.worksheet.write(self.row_count, 31, '即时主队水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 32, '即时盘口'.encode('utf-8'))
        self.worksheet.write(self.row_count, 33, '即时客队水位'.encode('utf-8'))
        # leave 34th. column empty
        self.worksheet.write(self.row_count, 35, '初盘大球水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 36, '初盘进球数'.encode('utf-8'))
        self.worksheet.write(self.row_count, 37, '初盘小球水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 38, '即时大球水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 39, '即时进球数'.encode('utf-8'))
        self.worksheet.write(self.row_count, 40, '即时小球水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 41, 'Crawl Link'.encode('utf-8'))
        self.worksheet.write(self.row_count, 42, '主队比分'.encode('utf-8'))
        self.worksheet.write(self.row_count, 43, '客队比分'.encode('utf-8'))
        self.row_count += 1

    def spider_closed(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        # print('item[%s] to be processed:' % (item['name']))

        if hasattr(item, 'season'):
            self.worksheet.write(self.row_count, 0, item['season'])
        if hasattr(item, 'round'):
            self.worksheet.write(self.row_count, 1, item['round'])
        if hasattr(item, 'match_time'):
            self.worksheet.write(self.row_count, 2, item['match_time'])
        if hasattr(item, 'scheduleid'):
            self.worksheet.write(self.row_count, 3, item['scheduleid'])
        if hasattr(item, 'hometeam'):
            self.worksheet.write(self.row_count, 4, item['hometeam'])
        if hasattr(item, 'guestteam'):
            self.worksheet.write(self.row_count, 5, item['guestteam'])
        if hasattr(item, 'home_points'):
            self.worksheet.write(self.row_count, 6, item['home_points'])
        if hasattr(item, 'guest_points'):
            self.worksheet.write(self.row_count, 7, item['guest_points'])
        if hasattr(item, 'home_ranking'):
            self.worksheet.write(self.row_count, 8, item['home_ranking'])
        if hasattr(item, 'guest_ranking'):
            self.worksheet.write(self.row_count, 9, item['guest_ranking'])
        if hasattr(item, 'home_win_ratio'):
            self.worksheet.write(self.row_count, 10, item['home_win_ratio'])
        if hasattr(item, 'guest_win_ratio'):
            self.worksheet.write(self.row_count, 11, item['guest_win_ratio'])
        # leave 12th. column empty
        if hasattr(item, 'home_win_of_last_6match'):
            self.worksheet.write(self.row_count, 13, item['home_win_of_last_6match'])
        if hasattr(item, 'home_draw_of_last_6match'):
            self.worksheet.write(self.row_count, 14, item['home_draw_of_last_6match'])
        if hasattr(item, 'home_lost_of_last_6match'):
            self.worksheet.write(self.row_count, 15, item['home_lost_of_last_6match'])
        # leave 16th. column empty
            self.worksheet.write(self.row_count, 17, item['guest_win_of_last_6match'])
        if hasattr(item, 'guest_draw_of_last_6match'):
            self.worksheet.write(self.row_count, 18, item['guest_draw_of_last_6match'])
        if hasattr(item, 'guest_lost_of_last_6match'):
            self.worksheet.write(self.row_count, 19, item['guest_lost_of_last_6match'])
        if hasattr(item, 'bookie_name_en'):
            self.worksheet.write(self.row_count, 20, item['bookie_name_en'])
        # 欧盘胜平负的赔率
        if hasattr(item, 'open_home_win'):
            self.worksheet.write(self.row_count, 21, item['open_home_win'])
        if hasattr(item, 'open_draw'):
            self.worksheet.write(self.row_count, 22, item['open_draw'])
        if hasattr(item, 'open_guest_win'):
            self.worksheet.write(self.row_count, 23, item['open_guest_win'])
        if hasattr(item, 'asian_start_homewager'):
            self.worksheet.write(self.row_count, 24, item['asian_start_homewager'])
        if hasattr(item, 'asian_start_handicap'):
            self.worksheet.write(self.row_count, 25, item['asian_start_handicap'])
        if hasattr(item, 'asian_start_guestwager'):
            self.worksheet.write(self.row_count, 26, item['asian_start_guestwager'])
        # leave 27th. column empty
        if hasattr(item, 'end_home_win'):
            self.worksheet.write(self.row_count, 28, item['end_home_win'])
        if hasattr(item, 'end_draw'):
            self.worksheet.write(self.row_count, 29, item['end_draw'])
        if hasattr(item, 'end_guest_win'):
            self.worksheet.write(self.row_count, 30, item['end_guest_win'])
        if hasattr(item, 'asian_end_homewager'):
            self.worksheet.write(self.row_count, 31, item['asian_end_homewager'])
        if hasattr(item, 'asian_end_handicap'):
            self.worksheet.write(self.row_count, 32, item['asian_end_handicap'])
        if hasattr(item, 'asian_end_guestwager'):
            self.worksheet.write(self.row_count, 33, item['asian_end_guestwager'])
        # leave 34th. column empty
        # 亚盘大小球水位
        if hasattr(item, 'asian_start_more_goal'):
            self.worksheet.write(self.row_count, 35, item['asian_start_more_goal'])
        if hasattr(item, 'asian_start_goal_total'):
            self.worksheet.write(self.row_count, 36, item['asian_start_goal_total'])
        if hasattr(item, 'asian_start_less_goal'):
            self.worksheet.write(self.row_count, 37, item['asian_start_less_goal'])
        if hasattr(item, 'asian_end_more_goal'):
            self.worksheet.write(self.row_count, 38, item['asian_end_more_goal'])
        if hasattr(item, 'asian_end_goal_total'):
            self.worksheet.write(self.row_count, 39, item['asian_end_goal_total'])
        if hasattr(item, 'asian_end_less_goal'):
            self.worksheet.write(self.row_count, 40, item['asian_end_less_goal'])
        self.worksheet.write(self.row_count, 41, item['crawling_link'])
        if hasattr(item, 'home_score'):
            self.worksheet.write(self.row_count, 42, item['home_score'])
        if hasattr(item, 'guest_score'):
            self.worksheet.write(self.row_count, 43, item['guest_score'])
        self.row_count += 1
        return item
