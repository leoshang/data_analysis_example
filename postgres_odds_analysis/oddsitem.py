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

    # 欧盘胜负平赔率
    open_home_win = scrapy.Field()
    open_draw = scrapy.Field()

    # 亚盘让球
    asian_start_home_wager = scrapy.Field()
    asian_start_handicap = scrapy.Field()

    # 亚盘大小球
    host_goal = scrapy.Field()
    guest_goal = scrapy.Field()

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    # in order to make call self.season successful, the following method has to be implemented
    # otherwise it has to call self['season']
    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, o):
        return self.__dict__ == o.__dict__

    def __lt__(self, other):
        return self.open_draw < other.open_draw


