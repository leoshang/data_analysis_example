# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# def serialize_weight(value):
#     weight = value.split(':')
#     return "=\"" + weight[1].strip() + "\""


class EuroOddsPipelineItem(scrapy.Item):
    # match_id, match_time,
    # bookie_id, bookie_name_en, bookie_name_cn,
    # matchday, season, matchname,
    # hometeam, guestteam,
    # hometeam_cn, guestteam_cn,
    # open_home_win, open_draw, open_guest_win,
    # end_home_win, end_draw, end_guest_win,
    # open_home_prob, open_draw_prob, open_guest_prob,
    # end_home_win_prob, end_draw_prob, end_guest_win_prob

    match_id = scrapy.Field()
    match_time = scrapy.Field()
    bookie_id = scrapy.Field()
    bookie_name_en = scrapy.Field()
    bookie_name_cn = scrapy.Field()

    matchday = scrapy.Field()
    season = scrapy.Field()
    matchname = scrapy.Field()
    hometeam = scrapy.Field()
    guestteam = scrapy.Field()
    hometeam_cn = scrapy.Field()
    guestteam_cn = scrapy.Field()

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

