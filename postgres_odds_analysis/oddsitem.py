# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# def serialize_weight(value):
#     weight = value.split(':')
#     return "=\"" + weight[1].strip() + "\""


class EuroOdds(scrapy.Item):
    # 欧盘机构
    bookie_name_en = scrapy.Field()

    # 主队
    home_team = scrapy.Field()

    # 主队基本面
    home_points = scrapy.Field()
    home_ranking = scrapy.Field()
    home_win_ratio = scrapy.Field()
    home_win_of_last_6match = scrapy.Field()
    home_draw_of_last_6match = scrapy.Field()
    home_lost_of_last_6match = scrapy.Field()

    # 客队
    guest_team = scrapy.Field()

    # 客队基本面
    guest_points = scrapy.Field()
    guest_ranking = scrapy.Field()
    guest_win_ratio = scrapy.Field()
    guest_win_of_last_6match =  scrapy.Field()
    guest_draw_of_last_6match = scrapy.Field()
    guest_lost_of_last_6match = scrapy.Field()

    # 欧盘胜负平赔率
    open_home_win = scrapy.Field()
    open_draw = scrapy.Field()
    open_guest_win = scrapy.Field()

    # 亚盘让球
    asian_start_home_wager = scrapy.Field()
    asian_start_handicap = scrapy.Field()
    asian_start_guest_wager = scrapy.Field()

    # 亚盘大小球
    asian_start_more_goal = scrapy.Field()
    asian_start_goal_total = scrapy.Field()
    asian_start_less_goal = scrapy.Field()

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    # in order to make call self.season successful, the following method has to be implemented
    # otherwise it has to call self['season']
    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return str(self.__dict__)


