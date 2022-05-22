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
        file_prefix = spider.league + '-' + spider.current_season
        self.workbook = xlsxwriter.Workbook('%s.xlsx' % file_prefix)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.set_default_row(25)
        self.output_header()

    def output_header(self):
        # self.worksheet.write(self.row_count, 5, self.odds_company_title)
        # matchday, season, matchname,
        # hometeam, guestteam,
        # hometeam_cn, guestteam_cn,
        # self.row_count += 1
        self.worksheet.write(self.row_count, 0, '联赛名称'.encode('utf-8'))
        self.worksheet.write(self.row_count, 1, '联赛Id'.encode('utf-8'))
        self.worksheet.write(self.row_count, 2, '赛季'.encode('utf-8'))
        self.worksheet.write(self.row_count, 3, '比赛日'.encode('utf-8'))
        self.worksheet.write(self.row_count, 4, '比赛时间'.encode('utf-8'))

        self.worksheet.write(self.row_count, 5, '主队'.encode('utf-8'))
        self.worksheet.write(self.row_count, 6, '主队中文'.encode('utf-8'))
        self.worksheet.write(self.row_count, 7, '主队积分'.encode('utf-8'))
        self.worksheet.write(self.row_count, 8, '主队排名'.encode('utf-8'))
        self.worksheet.write(self.row_count, 9, '主队胜率'.encode('utf-8'))
        self.worksheet.write(self.row_count, 10, '主队近六场赢'.encode('utf-8'))
        self.worksheet.write(self.row_count, 11, '主队近六场平'.encode('utf-8'))
        self.worksheet.write(self.row_count, 12, '主队近六场负'.encode('utf-8'))

        self.worksheet.write(self.row_count, 13, '客队'.encode('utf-8'))
        self.worksheet.write(self.row_count, 14, '客队中文'.encode('utf-8'))
        self.worksheet.write(self.row_count, 15, '客队积分'.encode('utf-8'))
        self.worksheet.write(self.row_count, 16, '客队排名'.encode('utf-8'))
        self.worksheet.write(self.row_count, 17, '客队胜率'.encode('utf-8'))
        self.worksheet.write(self.row_count, 18, '客队近六场赢'.encode('utf-8'))
        self.worksheet.write(self.row_count, 19, '客队近六场平'.encode('utf-8'))
        self.worksheet.write(self.row_count, 20, '客队近六场负'.encode('utf-8'))

        self.worksheet.write(self.row_count, 21, '博彩公司Id'.encode('utf-8'))
        self.worksheet.write(self.row_count, 22, '博彩公司英文名称'.encode('utf-8'))
        self.worksheet.write(self.row_count, 23, '博彩公司中文名称'.encode('utf-8'))

        self.worksheet.write(self.row_count, 24, '初盘主胜赔付'.encode('utf-8'))
        self.worksheet.write(self.row_count, 25, '初盘平局赔付'.encode('utf-8'))
        self.worksheet.write(self.row_count, 26, '初盘客胜赔付'.encode('utf-8'))

        self.worksheet.write(self.row_count, 27, '即时终盘主胜赔付'.encode('utf-8'))
        self.worksheet.write(self.row_count, 28, '即时终盘平局赔付'.encode('utf-8'))
        self.worksheet.write(self.row_count, 29, '即时终盘客胜赔付'.encode('utf-8'))

        self.worksheet.write(self.row_count, 30, '初盘主胜概率'.encode('utf-8'))
        self.worksheet.write(self.row_count, 31, '初盘主胜概率'.encode('utf-8'))
        self.worksheet.write(self.row_count, 32, '初盘主胜概率'.encode('utf-8'))

        self.worksheet.write(self.row_count, 33, '即时终盘主胜概率'.encode('utf-8'))
        self.worksheet.write(self.row_count, 34, '即时终盘平局概率'.encode('utf-8'))
        self.worksheet.write(self.row_count, 35, '即时终盘客胜概率'.encode('utf-8'))

        self.worksheet.write(self.row_count, 36, '亚盘公司'.encode('utf-8'))
        self.worksheet.write(self.row_count, 37, '初盘主队水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 38, '初盘盘口'.encode('utf-8'))
        self.worksheet.write(self.row_count, 39, '初盘客队水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 40, '即时主队水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 41, '即时盘口'.encode('utf-8'))
        self.worksheet.write(self.row_count, 42, '即时客队水位'.encode('utf-8'))
        self.worksheet.write(self.row_count, 43, 'Crawl Link'.encode('utf-8'))
        self.row_count += 1

    def spider_closed(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        # print('item[%s] to be processed:' % (item['name']))
        if hasattr(item, 'matchname'):
            self.worksheet.write(self.row_count, 0, item['matchname'])
        if hasattr(item, 'match_id'):
            self.worksheet.write(self.row_count, 1, item['match_id'])
        if hasattr(item, 'season'):
            self.worksheet.write(self.row_count, 2, item['season'])
        if hasattr(item, 'matchday'):
            self.worksheet.write(self.row_count, 3, item['matchday'])
        if hasattr(item, 'match_time'):
            self.worksheet.write(self.row_count, 4, item['match_time'])

        if hasattr(item, 'hometeam'):
            self.worksheet.write(self.row_count, 5, item['hometeam'])
        if hasattr(item, 'hometeam_cn'):
            self.worksheet.write(self.row_count, 6, item['hometeam_cn'])
        if hasattr(item, 'home_points'):
            self.worksheet.write(self.row_count, 7, item['home_points'])
        if hasattr(item, 'home_ranking'):
            self.worksheet.write(self.row_count, 8, item['home_ranking'])
        if hasattr(item, 'home_win_ratio'):
            self.worksheet.write(self.row_count, 9, item['home_win_ratio'])
        if hasattr(item, 'home_win_of_last_6match'):
            self.worksheet.write(self.row_count, 10, item['home_win_of_last_6match'])
        if hasattr(item, 'home_draw_of_last_6match'):
            self.worksheet.write(self.row_count, 11, item['home_draw_of_last_6match'])
        if hasattr(item, 'home_lost_of_last_6match'):
            self.worksheet.write(self.row_count, 12, item['home_lost_of_last_6match'])

        if hasattr(item, 'guestteam'):
            self.worksheet.write(self.row_count, 13, item['guestteam'])
        if hasattr(item, 'guestteam_cn'):
            self.worksheet.write(self.row_count, 14, item['guestteam_cn'])
        if hasattr(item, 'guest_points'):
            self.worksheet.write(self.row_count, 15, item['guest_points'])
        if hasattr(item, 'guest_ranking'):
            self.worksheet.write(self.row_count, 16, item['guest_ranking'])
        if hasattr(item, 'guest_win_ratio'):
            self.worksheet.write(self.row_count, 17, item['guest_win_ratio'])
        if hasattr(item, 'guest_win_of_last_6match'):
            self.worksheet.write(self.row_count, 18, item['guest_win_of_last_6match'])
        if hasattr(item, 'guest_draw_of_last_6match'):
            self.worksheet.write(self.row_count, 19, item['guest_draw_of_last_6match'])
        if hasattr(item, 'guest_lost_of_last_6match'):
            self.worksheet.write(self.row_count, 20, item['guest_lost_of_last_6match'])

        if hasattr(item, 'bookie_id'):
            self.worksheet.write(self.row_count, 21, item['bookie_id'])
        if hasattr(item, 'bookie_name_en'):
            self.worksheet.write(self.row_count, 22, item['bookie_name_en'])
        if hasattr(item, 'bookie_name_cn'):
            self.worksheet.write(self.row_count, 23, item['bookie_name_cn'])

        if hasattr(item, 'open_home_win'):
            self.worksheet.write(self.row_count, 24, item['open_home_win'])
        if hasattr(item, 'open_draw'):
            self.worksheet.write(self.row_count, 25, item['open_draw'])
        if hasattr(item, 'open_guest_win'):
            self.worksheet.write(self.row_count, 26, item['open_guest_win'])

        if hasattr(item, 'end_home_win'):
            self.worksheet.write(self.row_count, 27, item['end_home_win'])
        if hasattr(item, 'end_draw'):
            self.worksheet.write(self.row_count, 28, item['end_draw'])
        if hasattr(item, 'end_guest_win'):
            self.worksheet.write(self.row_count, 29, item['end_guest_win'])

        if hasattr(item, 'open_home_prob'):
            self.worksheet.write(self.row_count, 30, item['open_home_prob'])
        if hasattr(item, 'open_draw_prob'):
            self.worksheet.write(self.row_count, 31, item['open_draw_prob'])
        if hasattr(item, 'open_guest_prob'):
            self.worksheet.write(self.row_count, 32, item['open_guest_prob'])

        if hasattr(item, 'end_home_win_prob'):
            self.worksheet.write(self.row_count, 33, item['end_home_win_prob'])
        if hasattr(item, 'end_draw_prob'):
            self.worksheet.write(self.row_count, 34, item['end_draw_prob'])
        if hasattr(item, 'end_guest_win_prob'):
            self.worksheet.write(self.row_count, 35, item['end_guest_win_prob'])

        if hasattr(item, 'asian_bookie'):
            self.worksheet.write(self.row_count, 36, item['asian_bookie'])
        if hasattr(item, 'asian_start_homewager'):
            self.worksheet.write(self.row_count, 37, item['asian_start_homewager'])
        if hasattr(item, 'asian_start_handicap'):
            self.worksheet.write(self.row_count, 38, item['asian_start_handicap'])
        if hasattr(item, 'asian_start_guestwager'):
            self.worksheet.write(self.row_count, 39, item['asian_start_guestwager'])
        if hasattr(item, 'asian_end_homewager'):
            self.worksheet.write(self.row_count, 40, item['asian_end_homewager'])
        if hasattr(item, 'asian_end_handicap'):
            self.worksheet.write(self.row_count, 41, item['asian_end_handicap'])
        if hasattr(item, 'asian_end_guestwager'):
            self.worksheet.write(self.row_count, 42, item['asian_end_guestwager'])
        self.worksheet.write(self.row_count, 43, item['crawling_link'])

        self.row_count += 1
        return item
