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
    # league name
    matchname = scrapy.Field()
    schedule_id = scrapy.Field()
    match_id = scrapy.Field()
    season = scrapy.Field()
    matchday = scrapy.Field()
    match_time = scrapy.Field()

    hometeam = scrapy.Field()
    hometeam_cn = scrapy.Field()
    hometeam_id = scrapy.Field()
    home_points = scrapy.Field()
    home_ranking = scrapy.Field()
    home_win_ratio = scrapy.Field()
    home_win_of_last_6match = scrapy.Field()
    home_draw_of_last_6match = scrapy.Field()
    home_lost_of_last_6match = scrapy.Field()

    guestteam = scrapy.Field()
    guestteam_cn = scrapy.Field()
    guestteam_id = scrapy.Field()
    guest_points = scrapy.Field()
    guest_ranking = scrapy.Field()
    guest_win_ratio = scrapy.Field()
    guest_win_of_last_6match =  scrapy.Field()
    guest_draw_of_last_6match = scrapy.Field()
    guest_lost_of_last_6match = scrapy.Field()

    bookie_id = scrapy.Field()
    bookie_name_en = scrapy.Field()
    bookie_name_cn = scrapy.Field()

    open_home_win = scrapy.Field()
    open_draw = scrapy.Field()
    open_guest_win = scrapy.Field()

    end_home_win = scrapy.Field()
    end_draw = scrapy.Field()
    end_guest_win = scrapy.Field()

    open_home_prob = scrapy.Field()
    open_draw_prob = scrapy.Field()
    open_guest_prob = scrapy.Field()

    end_home_win_prob = scrapy.Field()
    end_draw_prob = scrapy.Field()
    end_guest_win_prob = scrapy.Field()

    asian_bookie = scrapy.Field()
    asian_start_homewager = scrapy.Field()
    asian_start_handicap = scrapy.Field()
    asian_start_guestwager = scrapy.Field()
    asian_end_homewager = scrapy.Field()
    asian_end_handicap = scrapy.Field()
    asian_end_guestwager = scrapy.Field()

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    # in order to make call self.season successful, the following method has to be implemented
    # otherwise it has to call self['season']
    def __getitem__(self, item):
        return self.__dict__[item]

    # def __str__(self):
    #     return str(self.__dict__)


