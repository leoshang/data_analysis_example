# -*- coding: utf-8 -*-
from __future__ import division
import scrapy

from sportsbook.responseinspector.eurooddsInspector import EuroOddsInspector
from sportsbook.responseinspector.sofascore_inspector import SofaScoreInspector
from sportsbook.spiders.sportsbook_config import SportsbookConfiguration

_JS_CHARSET_LOC_ = '" charset'
_JS_SRC_LOC_ = "src="
_JS_SUFFIX_ = '.js'
_JS_DOMAIN_ = 'http://1x2d.win007.com/'
SCRIPT_TAG = "//script[@src]"
_UTF_8_ = "utf-8"
item_count = 0


class SportsbookJavascriptParser(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "sportsbookspider"
    allowed_domains = ["win007.com"]

    def __init__(self, *a, **kw):
        self.start_urls = []
        self.append_match_url(SportsbookConfiguration.get_season_round_url(),
                              SportsbookConfiguration.get_current_season(),
                              SportsbookConfiguration.get_round_total())
        self.euroodds_inspector = EuroOddsInspector()
        self.sofascore_inspector = SofaScoreInspector()
        print(self.start_urls)

    def append_match_url(self, start_url, current_season, round_total):
        for r in range(int(str(round_total))):
            match_url = str(start_url).replace('$1', current_season).replace('$2', str(r + 1))
            self.start_urls.append(match_url)

    def parse(self, response):
        match_bloc = response.body.encode(_UTF_8_)
        match_array = match_bloc.split(";")
        for m in match_array:
            matchid = self.extract_matchid(m)
            if not matchid:
                # print str(m) + "match has no id"
                continue
            e_odds_url = SportsbookConfiguration.get_euro_odds_site().replace("$matchId", str(matchid)).encode("UTF-8")
            a_odds_url = SportsbookConfiguration.get_asian_odds_site().replace("$matchId", matchid).encode("UTF-8")
            analysis_url = SportsbookConfiguration.get_analysis_site().replace("$matchId", matchid).encode("UTF-8")
            request_euroodds = scrapy.Request(e_odds_url, callback=self.parse_odds,
                                              meta={'asian_odds_link': a_odds_url,
                                                    'analysis_link': analysis_url})
            yield request_euroodds

    def parse_odds(self, response):
        odds_rows = response.xpath(SCRIPT_TAG)
        asian_odds_url = response.meta.get('asian_odds_link')
        analysis_url = response.meta.get('analysis_link')
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
                                                            'current_season': SportsbookConfiguration.get_current_season()})
                    yield request_euroodds
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
