# -*- coding: utf-8 -*-
from __future__ import division
import scrapy
import configparser

from sportsbook.responseinspector.eurooddsInspector import EuroOddsInspector
# absolute path:= /Users/leoshang/workspace/football_data_analysis/sportsbook/sportsbook/spiders/
from sportsbook.responseinspector.sofascore_inspector import SofaScoreInspector

_SPORTSBOOK_CONFIG_FILE_ = '/Users/leoshang/workspace/football_data_analysis/sportsbook/sportsbook/spiders/premier-league.ini'
_JS_CHARSET_LOC_ = '" charset'
_JS_SRC_LOC_ = "src="
_JS_SUFFIX_ = '.js'
_JS_DOMAIN_ = 'http://1x2d.win007.com/'
_UTF_8_ = "utf-8"

CURRENT_SEASON = 2014


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
        self.start_urls = []
        start_url = SportsbookJavascriptParser.config_section_map('PremierLeague')['season_round_url']
        season_list = SportsbookJavascriptParser.config_section_map('PremierLeague')['all_season']
        round_total = SportsbookJavascriptParser.config_section_map('PremierLeague')['round_total']
        self.euro_odds_url = SportsbookJavascriptParser.config_section_map('PremierLeague')['euro_odds_site']
        self.asian_odds_url = SportsbookJavascriptParser.config_section_map('PremierLeague')['asian_odds_site']
        self.analysis_url = SportsbookJavascriptParser.config_section_map('PremierLeague')['analysis_site']

        self.append_match_url(start_url, season_list, round_total)
        self.odds_team_title = ''
        self.euroodds_inspector = EuroOddsInspector()
        self.sofascore_inspector = SofaScoreInspector()
        print(self.start_urls)

    SCRIPT_TAG = "//script[@src]"
    item_count = 0

    def append_match_url(self, start_url, season_list, round_total):
        season_array = str(season_list).split(",")
        for season in season_array:
            for r in range(int(str(round_total))):
                match_url = str(start_url).replace('$1', season).replace('$2', str(r+1))
                self.start_urls.append(match_url)
                # print "match: " + match_url

    def parse(self, response):
        # print response.request.headers['User-Agent']
        # print response.request.headers.get('Referrer', None)

        match_bloc = response.body.encode(_UTF_8_)
        match_array = match_bloc.split(";")
        # print len(match_array)
        for m in match_array:
            matchid = self.extract_matchid(m)
            if not matchid:
                # print str(m) + "match has no id"
                continue
            current_season = response.url[response.url.index("matchSeason") + 12: response.url.index("matchSeason") + 21]
            e_odds_url = self.euro_odds_url.replace("$matchId", str(matchid)).encode("UTF-8")
            a_odds_url = self.asian_odds_url.replace("$matchId", matchid).encode("UTF-8")
            analysis_url = self.analysis_url.replace("$matchId", matchid).encode("UTF-8")
            request_euroodds = scrapy.Request(e_odds_url, callback=self.parse_odds,
                                              meta={'asian_odds_link': a_odds_url,
                                                    'analysis_link': analysis_url,
                                                    'current_season': current_season})
            yield request_euroodds

    def parse_odds(self, response):
        odds_rows = response.xpath(self.SCRIPT_TAG)
        asian_odds_url = response.meta.get('asian_odds_link')
        analysis_url = response.meta.get('analysis_link')
        current_season = response.meta.get('current_season')
        for index, odd_row in enumerate(odds_rows):
            script_tag = odd_row.extract().encode(_UTF_8_)
            print(script_tag)
            idx_begin = script_tag.index(_JS_SRC_LOC_)
            if _JS_CHARSET_LOC_ not in script_tag or _JS_SRC_LOC_ not in script_tag:
                continue
            idx_end = script_tag.index(_JS_CHARSET_LOC_)
            # print(idx_begin)
            # print(idx_end)
            if idx_begin > 0 and idx_end > 0:
                script_link = script_tag[idx_begin + 5:idx_end]
                if script_link.startswith(_JS_DOMAIN_) and _JS_SUFFIX_ in script_link:
                    print 'target javascript site found' + script_link
                    request_euroodds = scrapy.Request(script_link, callback=self.euroodds_inspector.extract_euro_odds,
                                                      meta={'scrapy_instance': scrapy,
                                                            'asian_odds_link': asian_odds_url,
                                                            'analysis_link': analysis_url,
                                                            'current_season': current_season})
                    yield request_euroodds

                    request_sofa = scrapy.Request("https://www.sofascore.com/football/2017-08-11",
                                                  callback=self.sofascore_inspector.extract_score)
                    # yield request_sofa
                    break
            else:
                break

    def extract_matchid(self, m):
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
