# -*- coding: utf-8 -*-
from __future__ import division
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
        self.start_urls = SportsbookConfiguration.get_all_asian_links()
        self.asian_odds_inspector = AsianOddsInspector()
        print(self.start_urls)

    def start_requests(self):
        for r in self.start_urls:
            request = scrapy.Request(r, callback=self.parse, priority=-r*30)
            yield request

    def parse(self, response):
        match_bloc = response.body.encode('utf-8')
        self.asian_odds_inspector.extract_euro_odds
        filtered_matches = list(map(str.strip, match_array))
        filtered_matches = filter(None, filtered_matches)

        for index, m in enumerate(filtered_matches):
            match_id = self.extract_match_id(m)
            if not match_id:
                print response.url + "match has no id"
                continue
            e_odds_url = self.e_odds_site.replace("$matchId", str(match_id)).encode("UTF-8")
            a_odds_url = self.a_odds_site.replace("$matchId", str(match_id)).encode("UTF-8")
            a_goal_url = self.a_goal_site.replace("$matchId", str(match_id)).encode("UTF-8")
            analysis_url = self.analysis_site.replace("$matchId", str(match_id)).encode("UTF-8")
            request_euro_odds = scrapy.Request(e_odds_url,
                                               callback=self.asian_odds_inspector.extract_euro_odds,
                                               priority=(int(current_round)-1)*index+1,
                                               meta={'scrapy_instance': scrapy,
                                                     'asian_odds_link': a_odds_url,
                                                     'asian_goal_link': a_goal_url,
                                                     'analysis_link': analysis_url,
                                                     'current_round': current_round})
            yield request_euro_odds

    # extract 851540 out of oddsData["O_851540"]=[[97,1.35,4.8,8], ...]]
    def extract_match_id(self, m):
        if not m or len(m) < 1 or ("=" not in m):
            return None
        m_array = m.split("=")
        # print m_array[0]
        tmp = m_array[0].replace("\"]", "")
        # print tmp
        id_array = tmp.split("_")
        if id_array and len(id_array) > 1:
            return id_array[1]
        else:
            return None

    def spider_closed(self, spider):
        print 'spider crawled ' + str(self.counter) + ' items'

    def item_scraped(self, item, response, spider):
        self.counter += 1

