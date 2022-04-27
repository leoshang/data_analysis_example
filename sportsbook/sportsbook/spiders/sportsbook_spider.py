# -*- coding: utf-8 -*-
from __future__ import division
import scrapy
import configparser

from sportsbook.items import EuroOdds
from sportsbook.responseinspector.asianoddsinspector import AsianOddsInspector
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
        self.euroodds_inspector = EuroOddsInspector()
        self.asianodds_inspector = AsianOddsInspector()
        print(self.start_urls)

    SCRIPT_TAG = "//script[@src]"

    # 比分
    # <div class="row" id="headVs">
    #     <div class="end">
    #         <div class="score">4</div>
    #         <div>
    #             <span class="row red b"> 完 </span>
    #             <span class="row"> (2-2) </span>
    #         </div>
    #         <div class="score"> 3 </div>
    #     </div>
    # </div>

    item_count = 0

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
                    break
            else:
                break
