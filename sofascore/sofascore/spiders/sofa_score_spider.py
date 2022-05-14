# -*- coding: utf-8 -*-
from __future__ import division
import scrapy
import configparser
import json

from sofascore.responseinspector.sofascore_inspector import SofaScoreInspector

_SOFA_SCORE_CONFIG_FILE_ = '/Users/leoshang/workspace/football_data_analysis/sofascore/sofascore/spiders/premier-league.ini'
_UTF_8_ = "utf-8"


class SofaScoreCrawler(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "sofascorespider"
    allowed_domains = ["sofascore.com"]
    data_feed_config = configparser.ConfigParser()
    data_feed_config.read(_SOFA_SCORE_CONFIG_FILE_)

    @staticmethod
    def config_section_map(section):
        dict1 = {}
        options = SofaScoreCrawler.data_feed_config.options(section)
        for option in options:
            try:
                dict1[option] = SofaScoreCrawler.data_feed_config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        # print(dict1)
        return dict1

    def __init__(self, *a, **kw):
        super(SofaScoreCrawler, self).__init__(*a, **kw)
        self.start_urls = []
        self.sofa_url = SofaScoreCrawler.config_section_map('PremierLeague')['sofa_site']
        self.sofa_season_site = SofaScoreCrawler.config_section_map('PremierLeague')['sofa_season_site']
        self.vote_site = SofaScoreCrawler.config_section_map('PremierLeague')['vote_site']
        self.current_season = SofaScoreCrawler.config_section_map('Season')['current_season']
        self.sofa_season_id = SofaScoreCrawler.config_section_map('Season')[self.current_season]
        self.sofa_season_site = self.sofa_season_site.replace('$season_id', self.sofa_season_id)
        self.start_urls.append(self.sofa_season_site)
        self.sofascore_inspector = SofaScoreInspector()
        print(self.start_urls)

    item_count = 0

    def parse(self, response):
        # print response.request.headers['User-Agent']
        # print response.request.headers.get('Referrer', None)

        all_match_data = json.loads(response.body.encode(_UTF_8_))
        data1_array = all_match_data['tournamentTeamEvents']['1']
        for match_key in data1_array.keys():
            for match in data1_array[match_key]:
                # print match['id']
                # print match['homeTeam']['name']
                # print match['homeTeam']['userCount']
                # print match['homeScore']['normaltime']
                # print match['awayTeam']['name']
                # print match['awayScore']['normaltime']
                # print match['awayTeam']['userCount']

                match_vote_url = self.vote_site.replace('$event_id', str(match['id']))
                print match_vote_url
                request_event = scrapy.Request(match_vote_url, callback=self.sofascore_inspector.extract_score,
                                               meta={'current_season': self.current_season})
                yield request_event
