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
    # define the combined primary key: matchname, hometeam, guestteam, matchday.
    matchname = scrapy.Field()
    matchday = scrapy.Field()
    hometeam = scrapy.Field()
    guestteam = scrapy.Field()

    matchname_cn = scrapy.Field()
    matchtime = scrapy.Field()
    hometeam_cn = scrapy.Field()
    guestteam_cn = scrapy.Field()
    season = scrapy.Field()

    institute_id = scrapy.Field()
    institute_name = scrapy.Field()
    # init_odds is type of EuroOdds
    init_odds = scrapy.Field()
    # final odds
    final_odds = scrapy.Field()
    calculated_init_asia_handicaps = scrapy.Field()
    calculated_final_asia_handicaps = scrapy.Field()

    #def __str__(self):
    #    return "matchname: {}; matchtime: {}; hometeam: {}; guestteam: {}; " \
    #           "season: {} ".format(self['matchname'], self['matchtime'],
    #                                                     self['hometeam'], self['guestteam'],
    #                                                     self['season'])


