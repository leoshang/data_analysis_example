# -*- coding: utf-8 -*-
from __future__ import division
import scrapy
from scrapy import Request

from sportsbook.responseinspector.analysisinspector import AnalysisInspector
from sportsbook.responseinspector.eurooddsInspector import EuroOddsInspector
from sportsbook.spiders.sportsbook_config import SportsbookConfiguration


class Win007(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "sportsbookspider"
    allowed_domains = ["titan007.com"]
    counter = 0

    def __init__(self, *a, **kw):
        self.start_urls = []
        self.current_round = 1
        self.euro_odds_inspector = EuroOddsInspector()
        self.e_odds_site = SportsbookConfiguration.get_euro_odds_site()
        self.a_odds_site = SportsbookConfiguration.get_asian_odds_site()
        self.analysis_site = SportsbookConfiguration.get_analysis_site()
        self.season_url = SportsbookConfiguration.get_season_round_url()\
            .replace('$1', SportsbookConfiguration.get_current_season())
        # self.start_urls.append(str(self.season_url).replace('$2', str(self.current_round)))
        # for r in range int(str(SportsbookConfiguration.get_round_total()))
        print(self.start_urls)

    def start_requests(self):
        next_round_url = str(self.season_url).replace('$2', str(self.current_round))
        request = scrapy.Request(next_round_url, callback=self.parse)
        yield request

    def parse(self, response):
        match_bloc = response.body.encode('utf-8')
        match_array = match_bloc.split(";")
        round_splitor = response.url.split("round=")
        current_round = round_splitor[1]
        for index, m in enumerate(match_array):
            match_id = self.extract_match_id(m)
            # the last two entries 30 and 31 are empty.
            if index < 30 and (not match_id):
                print response.url + "match has no id"
                continue
            e_odds_url = self.e_odds_site.replace("$matchId", str(match_id)).encode("UTF-8")
            a_odds_url = self.a_odds_site.replace("$matchId", str(match_id)).encode("UTF-8")
            analysis_url = self.analysis_site.replace("$matchId", str(match_id)).encode("UTF-8")
            request_euro_odds = scrapy.Request(e_odds_url,
                                               callback=self.euro_odds_inspector.extract_euro_odds,
                                               meta={'scrapy_instance': scrapy,
                                                     'asian_odds_link': a_odds_url,
                                                     'analysis_link': analysis_url,
                                                     'current_round': current_round})
            yield request_euro_odds
            Win007.counter += 1

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
