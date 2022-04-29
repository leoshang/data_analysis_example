# -*- coding: utf-8 -*-
from __future__ import division
import scrapy
import configparser

from sportsbook.items import EuroOdds
from sportsbook.responseinspector.asianoddsinspector import AsianOddsInspector
from sportsbook.responseinspector.eurooddsInspector import EuroOddsInspector

# absolute path:= /Users/leoshang/workspace/football_data_analysis/sportsbook/sportsbook/spiders/
from sportsbook.responseinspector.sofascore_inspector import SofaScoreInspector

_SPORTSBOOK_CONFIG_FILE_ = '/Users/leoshang/workspace/football_data_analysis/sportsbook/sportsbook/spiders/premiereleague-2017-2018.ini'
_JS_CHARSET_LOC_ = '" charset'
_JS_SRC_LOC_ = "src="
_JS_SUFFIX_ = '.js'
_JS_DOMAIN_ = 'http://1x2d.win007.com/'
_UTF_8_ = "utf-8"


class SportsbookJavascriptParser(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "sportsbookspider"
    allowed_domains = ["win007.com"]
    data_feed_config = configparser.ConfigParser()
    data_feed_config.read(_SPORTSBOOK_CONFIG_FILE_)

    @staticmethod
    def config_section_map(section):
        dict1 = {}
        options = SportsbookJavascriptParser.data_feed_config.options(section)
        for option in options:
            try:
                dict1[option] = SportsbookJavascriptParser.data_feed_config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        # print(dict1)
        return dict1

    def __init__(self, *a, **kw):
        # print(SportsbookJavascriptParser.data_feed_config.sections())
        super(SportsbookJavascriptParser, self).__init__(*a, **kw)
        start_url = SportsbookJavascriptParser.config_section_map('PremierLeague')['season_round_url']
        season_list = SportsbookJavascriptParser.config_section_map('PremierLeague')['all_season']
        round_total = SportsbookJavascriptParser.config_section_map('PremierLeague')['round_total']
        self.build_match_url(start_url, season_list, round_total)
        self.start_urls = []
        self.odds_team_title = ''
        self.start_urls.append(start_url)
        self.euroodds_inspector = EuroOddsInspector()
        self.asianodds_inspector = AsianOddsInspector()
        self.sofascore_inspector = SofaScoreInspector()
        print(self.start_urls)

    SCRIPT_TAG = "//script[@src]"
    item_count = 0

    def build_match_url(self, start_url, season_list, round_total):
        season_array = str(season_list).split(",")
        for season in season_array:
            for r in range(int(str(round_total))):
                match_url = str(start_url).replace('$1', season).replace('$2', str(r+1))
                print "match: " + match_url

    def parse(self, response):
        # print response.request.headers['User-Agent']
        # print response.request.headers.get('Referrer', None)
        odds_rows = response.xpath(self.SCRIPT_TAG)
        for index, odd_row in enumerate(odds_rows):
            script_tag = odd_row.extract().encode(_UTF_8_)
            print(script_tag)
            idx_begin = script_tag.index(_JS_SRC_LOC_)
            if _JS_CHARSET_LOC_ not in script_tag or _JS_SRC_LOC_ not in script_tag:
                continue
            idx_end = script_tag.index(_JS_CHARSET_LOC_)
            print(idx_begin)
            print(idx_end)
            if idx_begin > 0 and idx_end > 0:
                script_link = script_tag[idx_begin + 5:idx_end]
                print(script_link)
                if script_link.startswith(_JS_DOMAIN_) and _JS_SUFFIX_ in script_link:
                    print('target javascript site found')
                    request_euroodds = scrapy.Request(script_link, callback=self.euroodds_inspector.extract_euro_odds)
                    yield request_euroodds
                    request_asianodds = scrapy.Request("http://vip.win007.com/AsianOdds_n.aspx?id=1394661&l=0",
                                                       callback=self.asianodds_inspector.extract_asian_odds)
                    yield request_asianodds

                    request_sofa = scrapy.Request("https://www.sofascore.com/football/2017-08-11",
                                                  callback=self.sofascore_inspector.extract_score)
                    # https://www.sofascore.com/tournament/football/england/premier-league/17 英超

                    # https://www.sofascore.com/arsenal-leicester-city/GR
                    yield request_sofa
                    break
            else:
                break
