# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SofascoreItem(scrapy.Item):
    match_id = scrapy.Field()
    startTimestamp = scrapy.Field()
    hometeam = scrapy.Field()
    hometeam_score = scrapy.Field()
    hometeam_fans = scrapy.Field()

    guestteam = scrapy.Field()
    guestteam_score = scrapy.Field()
    guestteam_fans = scrapy.Field()

    vote_home_win = scrapy.Field()
    vote_draw = scrapy.Field()
    vote_guest_win = scrapy.Field()

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    # in order to make call self.season successful, the following method has to be implemented
    # otherwise it has to call self['season']
    def __getitem__(self, item):
        return self.__dict__[item]
