# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# def serialize_weight(value):
#     weight = value.split(':')
#     return "=\"" + weight[1].strip() + "\""


class AsianOdds(scrapy.Item):
    schedule_id = scrapy.Field()

    # 亚盘让球
    asian_start_homewager = scrapy.Field()
    asian_start_handicap = scrapy.Field()
    asian_start_guestwager = scrapy.Field()
    asian_end_homewager = scrapy.Field()
    asian_end_handicap = scrapy.Field()
    asian_end_guestwager = scrapy.Field()

    # 亚盘大小球
    # asian_start_more_goal = scrapy.Field()
    # asian_start_goal_total = scrapy.Field()
    # asian_start_less_goal = scrapy.Field()
    # asian_end_more_goal = scrapy.Field()
    # asian_end_goal_total = scrapy.Field()
    # asian_end_less_goal = scrapy.Field()

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    # in order to make call self.season successful, the following method has to be implemented
    # otherwise it has to call self['season']
    def __getitem__(self, item):
        return self.__dict__[item]

    # def __str__(self):
    #     return str(self.__dict__)
