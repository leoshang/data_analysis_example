# -*- coding: utf-8 -*-
from __future__ import division
import scrapy
import configparser

from sportsbook.responseinspector.eurooddsInspector import EuroOddsInspector

# absolute path:= /Users/leoshang/workspace/football_data_analysis/sportsbook/sportsbook/spiders/
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
        start_url = SportsbookJavascriptParser.config_section_map('General')['start_urls']
        self.start_urls = []
        self.odds_team_title = ''
        self.start_urls.append(start_url)
        self.response_inspector = EuroOddsInspector()
        print(self.start_urls)

    # ODDS_TEAM_TITLE_PATH = "//div[@id='TitleLeft']"

    ODDS_TABLE_ID = "//table[@id='oddsList_tab']"
    SCRIPT_TAG = "//script[@src]"
    ODD_ROW_PATH = "//tr[@align='center']"
    ODD_SEASON_ROUND_PATH = "td[0]/text()"
    ODD_SEASON_MATCH_DATE_PATH = "td[1]/text()"
    ODD_HOST_NAME_PATH = "td[2]/a/text()"
    ODD_HOST_RANKING_PATH = "td[2]/sup/text()"
    ODD_SCORE_PATH = "td[3]//strong/text()"
    ODD_GUEST_NAME_PATH = "td[4]/a/text()"
    ODD_GUEST_RANKING_PATH = "td[4]/sup/text()"
    ODD_ASIA_HANDICAP_PATH = "td[5]/text()"
    ODD_EURO_BET_LINK_PATH = "td[9]//a[1]/text()"

    item_count = 0

    # start_urls = [amazon_cn_search_result_link + "%s" % n for n in product_ids]

    # TODO FIX the crawling is recursively crawling the link in endless cycle!
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
                    request = scrapy.Request(script_link, callback=self.response_inspector.extract_euro_odds)
                    yield request
                    break
            else:
                break
            # citem = SportsbookItem()
            # yield citem


