# -*- coding: utf-8 -*-
from __future__ import division

import re

import scrapy
import time
from scrapy.crawler import signals
from pydispatch import dispatcher

from asianbookie.sportsbook.spiders.sportsbook_config import SportsbookConfiguration
from asianbookie.sportsbook.responseinspector.asianoddsinspector import AsianOddsInspector


class Win007(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "asianoddsspider"
    allowed_domains = ["titan007.com"]

    def __init__(self, *a, **kw):
        dispatcher.connect(self.item_scraped, signal=signals.item_scraped)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        self.counter = 0
        self.asian_odds_dict = {}
        self.start_urls = SportsbookConfiguration.get_all_asian_links().split(',')
        self.asian_odds_inspector = AsianOddsInspector()
        print(self.start_urls)

    def start_requests(self):
        for r in self.start_urls:
            asian_odds_url = re.sub(r"[\\\n\t\s]*", "", r)
            schedule_id = self.retrieve_schedule_id(asian_odds_url)
            request = scrapy.Request(asian_odds_url, callback=self.parse,
                                     method='GET', headers=None, body=None,
                                     cookies=None,
                                     meta={'ScheduleID': schedule_id},
                                     encoding='gb18030', priority=0,
                                     dont_filter=False, errback=None, flags=None, cb_kwargs=None
                                     )
            # request = request.replace(encoding='gb18030')
            yield request

    def parse(self, response):
        schedule_id = response.meta.get('ScheduleID')
        asian_odd = self.asian_odds_inspector.handle_asian_odd(response)
        asian_odd['schedule_id'] = schedule_id
        yield asian_odd

    # schedule id is the identifier of the match.
    def retrieve_schedule_id(self, asian_odds_url):
        # http: // vip.titan007.com / AsianOdds_n.aspx?id = 851849
        tmp = asian_odds_url.split("?")
        tmp = str(tmp[1]).split("=")
        return tmp[1]

    def spider_closed(self, spider):
        print 'spider crawled ' + str(self.counter) + ' items'

    def item_scraped(self, item, response, spider):
        self.counter += 1

