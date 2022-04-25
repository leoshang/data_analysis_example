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
    hometeam_id = scrapy.Field()
    horder = scrapy.Field()
    guestteam = scrapy.Field()
    guestteam_id = scrapy.Field()
    gorder = scrapy.Field()
    hometeam_cn = scrapy.Field()
    guestteam_cn = scrapy.Field()

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

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    # in order to make call self.season successful, the following method has to be implemented
    # otherwise it has to call self['season']
    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return "赛季：{}；比赛日：{}" \
               "比赛: {}; 主队: {}; 主队排名: {};" \
               "客队: {}; 客队排名: {};" \
               "赔率机构Id：{}；赔率机构名称：{}" \
               "初赔主胜: {}; 初赔平局: {}; 初赔客胜: {};" \
               "即时终赔主胜: {}; 即时终赔平局: {}; 即时终赔客胜: {};" \
               "初赔主胜（换算）概率: {}; " \
               "初赔平局（换算）概率: {}; " \
               "初赔客胜（换算）概率: {};" \
               "终赔主胜（换算）概率: {}; " \
               "终赔平局（换算）概率: {}; " \
               "终赔客胜（换算）概率: {}".format(
                self['season'], self.matchday,
                self.matchname, self.hometeam_cn, self.horder,
                self.guestteam_cn, self.gorder,
                self.bookie_id, self.bookie_name_cn,
                self.open_home_win, self.open_draw, self.open_guest_win,
                self.end_home_win, self.end_draw, self.end_guest_win,
                self.open_home_prob, self.open_draw_prob, self.open_guest_prob,
                self.end_home_win_prob, self.end_draw_prob, self.end_guest_win_prob)



