# -*- coding: utf-8 -*-
from __future__ import division

import re

import scrapy
import time
from scrapy.crawler import signals
from pydispatch import dispatcher

from sportsbook.spiders.sportsbook_config import SportsbookConfiguration

from sportsbook.responseinspector.asianoddsinspector import AsianOddsInspector


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
            request = scrapy.Request(asian_odds_url, callback=self.parse)
            yield request

    def parse(self, response):
        match_bloc = response.body.encode('utf-8')
        asian_odds = self.asian_odds_inspector.handle_asian_odds(response)
        if asian_odds['asian_start_handicap'] in self.asian_odds_dict:
            self.asian_odds_dict[asian_odds['asian_start_handicap']].append(asian_odds)
        else:
            self.asian_odds_dict[asian_odds['asian_start_handicap']] = [asian_odds]
        print asian_odds

    def spider_closed(self, spider):
        print 'spider crawled ' + str(self.counter) + ' items'

    def item_scraped(self, item, response, spider):
        self.counter += 1

