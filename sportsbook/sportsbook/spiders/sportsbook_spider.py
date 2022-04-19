# -*- coding: utf-8 -*-
from __future__ import division
import scrapy
import configparser
import re
from sportsbook.spiders.EuroOdds import EuroOdds
from sportsbook.spiders.AsiaOdds import AsiaOdds
from sportsbook.spiders.MatchEuroOdds import MatchEuroOdds
from sportsbook.spiders.MatchAsiaHandicap import MatchAsiaHandicap
from sportsbook.items import EuroOddsPipelineItem

# absolute path:= /Users/leoshang/workspace/football_data_analysis/sportsbook/sportsbook/spiders/
_SPORTSBOOK_CONFIG_FILE_ = '/Users/leoshang/workspace/football_data_analysis/sportsbook/sportsbook/spiders/premiereleague-2017-2018.ini'

_KEY_MATCH_DAY_ = 'matchday'
_KEY_INSTITUTION_NAME_ = 'institution_name'
_KEY_MATCH_TIME_ = 'matchtime'

_JS_VAR_GAME_DETAIL_ = 'gameDetail'
_JS_VAR_GAME_ = 'game'
_JS_VAR_ = 'var '
_JS_VAR_SCHEDULE_ = '";Schedule'
_JS_CHARSET_LOC_ = '" charset'
_JS_SRC_LOC_ = "src="
_JS_SUFFIX_ = '.js'
_JS_DOMAIN_ = 'http://1x2d.win007.com/'

_SPLITTOR_VAR_ = ';var '
_UTF_8_ = "utf-8"


class SportsbookJavascriptParser(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "sportsbookspider"
    allowed_domains = ["win007.com"]
    data_feed_config = configparser.ConfigParser()
    data_feed_config.read(_SPORTSBOOK_CONFIG_FILE_)

    match_fields = ['matchname', 'matchday', 'hometeam', 'guestteam',
                    'hometeam_cn', 'guestteam_cn', 'season']

    institue_list = ['Ladbrokes', 'Oddset', 'William Hill']

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
                    request = scrapy.Request(script_link, callback=self.extract_euro_odds)
                    yield request
                    break
            else:
                break
            # citem = SportsbookItem()
            # yield citem

    def extract_euro_odds(self, response):
        all_odds = response.text.encode(_UTF_8_)
        # print(all_odds)
        # @TODO populate later match_euro_odds into eu_pipeline_item
        eu_pipeline_item = EuroOddsPipelineItem()
        euro_odds = EuroOdds()
        all_odds_oneline = re.sub(r'\r\n', '', all_odds)
        var_list = all_odds_oneline.split(_SPLITTOR_VAR_)

        # for each var, filter the desired and populate it to match item
        for v in var_list:
            self.populate_match_odds(v, euro_odds)
        # print(euro_odds_item)

    def cleanup_jsdata(self, js_record):
        js_var = js_record.encode(_UTF_8_)
        if _JS_VAR_ in js_var:
            js_var = js_var[len(_JS_VAR_):]
        if '="' in js_var:
            js_var = js_var.replace('="', '=')
        if js_var.endswith('"'):
            js_var = js_var[:-1]
        elif js_var.endswith('";'):
            js_var = js_var[:-2]
        if _JS_VAR_SCHEDULE_ in js_var:
            idx = js_var.index(_JS_VAR_SCHEDULE_)
            js_var = js_var[:idx]
        # print(js_var)
        return js_var

    def populate_match_odds(self, js_record, euro_odds):
        js_var = self.cleanup_jsdata(js_record)
        # print(js_var)
        var_key_val = js_var.split("=")
        # print(var_key_val)
        if _KEY_MATCH_TIME_ == var_key_val[0].lower():
            self.extract_matchday(var_key_val[1], euro_odds)

        if var_key_val[0].lower() in self.match_fields:
            euro_odds[var_key_val[0].lower()] = var_key_val[1]

        if var_key_val[0] == _JS_VAR_GAME_:
            self.extract_all_game_odds(var_key_val[1], euro_odds)

        if var_key_val[0] == _JS_VAR_GAME_DETAIL_:
            self.handle_game_detail(var_key_val[1], euro_odds)

    def extract_matchday(self, match_datetime, euro_odds):
        # '2017,08-1,11,18,45,00'
        tm = match_datetime.split(',')
        matchday = tm[0] + '-' + tm[1]
        # print(matchday)
        euro_odds[_KEY_MATCH_DAY_] = matchday

    def extract_all_game_odds(self, game, euro_odds):
        vendorlist = self.cleanup_var_game(game)
        # print(vendorlist)
        # print(len(vendorlist))
        for item in vendorlist:
            itemstr = item.encode(_UTF_8_)
            self.append_institution_odds(itemstr, euro_odds)

    def append_institution_odds(self, oddstr, euro_odds):
        odds_values = oddstr.split('|')
        # print(odds_values[2]) # institue_name
        if odds_values[2] in self.institue_list:
            # print(oddstr)
            euro_odds['match_id'] = odds_values[0]
            euro_odds['match_time'] = odds_values[20]
            euro_odds['bookie_id'] = odds_values[1]
            euro_odds['bookie_name_en'] = odds_values[2]
            euro_odds['bookie_name_cn'] = odds_values[21]
            euro_odds['open_home_win'] = odds_values[3]
            euro_odds['open_draw'] = odds_values[4]
            euro_odds['open_guest_win'] = odds_values[5]
            euro_odds['end_home_win'] = odds_values[10]
            euro_odds['end_draw'] = odds_values[11]
            euro_odds['end_guest_win'] = odds_values[12]
            euro_odds['open_home_prob'] = odds_values[6]
            euro_odds['open_draw_prob'] = odds_values[7]
            euro_odds['open_guest_prob'] = odds_values[8]
            euro_odds['end_home_win_prob'] = odds_values[13]
            euro_odds['end_draw_prob'] = odds_values[14]
            euro_odds['end_guest_win_prob'] = odds_values[15]
            print euro_odds.__str__().encode(_UTF_8_)
        pass

    def cleanup_var_game(self, game):
        if game.startswith('Array("'):
            game = game.replace('Array("', '')
        if game.endswith('")'):
            game = game.replace('")', '')
        vendorlist = game.split('","')
        return vendorlist

    def handle_game_detail(self, game_details, match_euro_odds):
        pass
