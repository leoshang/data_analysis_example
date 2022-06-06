# -*- coding: utf-8 -*-
import re

from sportsbook.items import EuroOdds
from sportsbook.responseinspector.asianoddsinspector import AsianOddsInspector
from sportsbook.spiders.sportsbook_config import SportsbookConfiguration

_UTF_8_ = "utf-8"
_JS_VAR_GAME_ = 'game'
_JS_VAR_ = 'var '


# EuroOdds returned in format of key=value from a javascript file
class EuroOddsInspector:

    def __init__(self):
        self.match_fields = ['matchname', 'hometeam', 'hometeamid', 'guestteam', 'guestteamid',
                             'hometeam_cn', 'guestteam_cn', 'horder', 'gorder']
        self.institute_list = ['Ladbrokes', 'Oddset', 'William Hill']
        self.asia_odds_inspector = AsianOddsInspector()
        pass

    def extract_euro_odds(self, response):
        all_odds = response.text.encode(_UTF_8_)
        scrapy_instance = response.meta.get("scrapy_instance")
        asian_odds_link = response.meta.get("asian_odds_link")
        analysis_link = response.meta.get("analysis_link")
        current_round = response.meta.get('current_round')
        total_matches = response.meta.get('total_matches')
        odds_array = []
        fixture_fields = {}
        all_odds_oneline = re.sub(r'\r\n', '', all_odds)
        # odds data are separated by ";"
        var_list = all_odds_oneline.split(";")
        # for each var, filter the desired and populate it to match item
        for v in var_list:
            self.populate(v, fixture_fields, odds_array)
        print 'bookie total: ' + str(len(odds_array))

        for x in odds_array:
            x['season'] = SportsbookConfiguration.get_current_season()
            x['crawling_link'] = asian_odds_link
            x['round'] = current_round
            x.update(fixture_fields)

        request_asia_odds = scrapy_instance.Request(asian_odds_link,
                                                    callback=self.asia_odds_inspector.extract_asian_odds,
                                                    meta={'euro_odds_array': odds_array,
                                                          'analysis_link': analysis_link,
                                                          'scrapy_instance': scrapy_instance,
                                                          'total_matches': total_matches})
        yield request_asia_odds

    def populate(self, js_record, fixture_fields, odds_array):
        js_var = self.remove_useless_chars(js_record)
        # print(js_var)
        var_key_val = js_var.split("=", 1)
        # print(var_key_val)

        if var_key_val[0].lower() in self.match_fields:
            fixture_fields[var_key_val[0].lower()] = var_key_val[1]

        elif var_key_val[0] == _JS_VAR_GAME_:
            self.extract_all_game_odds(var_key_val[1], odds_array)

    def extract_all_game_odds(self, game, odds_array):
        bookies_euro_odds = self.cleanup_var_game(game)
        # print(all_euro_odds)
        # print(len(all_euro_odds))
        for bookie in bookies_euro_odds:
            bookie_odds = bookie.encode(_UTF_8_)
            self.build_euro_odds(bookie_odds, odds_array)

    def build_euro_odds(self, bookie_odds, odds_array):
        odds_values = bookie_odds.split('|')
        # print(odds_values[2]) # institue_name
        if odds_values[2] in self.institute_list:
            # print(oddstr)
            euro_odds = EuroOdds()
            euro_odds['match_id'] = odds_values[0]
            # euro_odds['match_time'] = odds_values[20]
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
            odds_array.append(euro_odds)
            # print euro_odds
        pass

    def remove_useless_chars(self, js_record):
        js_var = js_record.encode(_UTF_8_)
        if _JS_VAR_ in js_var:
            js_var = js_var[len(_JS_VAR_):]
        if '="' in js_var:
            js_var = js_var.replace('="', '=')
        if js_var.endswith('"'):
            js_var = js_var[:-1]
        elif js_var.endswith('";'):
            js_var = js_var[:-2]
        # print(js_var)
        return js_var

    def cleanup_var_game(self, game):
        if game.startswith('Array("'):
            game = game.replace('Array("', '')
        if game.endswith('")'):
            game = game.replace('")', '')
        vendorlist = game.split('","')
        return vendorlist

    def handle_game_detail(self, game_details, match_euro_odds):
        pass
