# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# def serialize_weight(value):
#     weight = value.split(':')
#     return "=\"" + weight[1].strip() + "\""


class AsianOdds:
    def __init__(self):
        self.season = None
        self.round = None
        # 菠菜机构
        self.bookie_name_en = None
        # 主队
        self.hometeam = None
        # 客队
        self.guestteam = None

        # 亚盘让球
        self.asian_start_homewager = None
        self.asian_start_handicap = None
        self.asian_start_guestwager = None
        self.asian_end_homewager = None
        self.asian_end_handicap = None
        self.asian_end_guestwager = None

        # 亚盘大小球
        asian_start_more_goal = None
        asian_start_goal_total = None
        asian_start_less_goal = None
        asian_end_more_goal = None
        asian_end_goal_total = None
        asian_end_less_goal = None

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    # in order to make call self.season successful, the following method has to be implemented
    # otherwise it has to call self['season']
    def __getitem__(self, item):
        return self.__dict__[item]
