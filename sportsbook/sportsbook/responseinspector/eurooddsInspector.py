import re

from sportsbook.items import EuroOdds

_UTF_8_ = "utf-8"
_JS_VAR_DELIMITER_ = ';'
_JS_VAR_MATCH_DAY_ = 'matchday'
_JS_VAR_MATCH_TIME_ = 'matchtime'
_JS_VAR_GAME_DETAIL_ = 'gameDetail'
_JS_VAR_GAME_ = 'game'
_JS_VAR_ = 'var '
_JS_VAR_SCHEDULE_ = 'Schedule='


# EuroOdds returned in format of key=value from a javascript file
class EuroOddsInspector:
    def __init__(self):
        self.match_fields = ['ScheduleID', 'matchname', 'matchday', 'hometeam', 'guestteam',
                        'hometeam_cn', 'guestteam_cn', 'season']
        self.institute_list = ['Ladbrokes', 'Oddset', 'William Hill']
        pass

    def extract_euro_odds(self, response):
        all_odds = response.text.encode(_UTF_8_)
        # print(all_odds)
        # @TODO populate later match_euro_odds into eu_pipeline_item
        euro_odds = EuroOdds()
        all_odds_oneline = re.sub(r'\r\n', '', all_odds)
        var_list = all_odds_oneline.split(_JS_VAR_DELIMITER_)
        # for each var, filter the desired and populate it to match item
        for v in var_list:
            self.extract(v, euro_odds)
            if hasattr(euro_odds, 'open_home_win') and euro_odds['open_home_win']:
                yield euro_odds

    def extract(self, js_record, euro_odds):
        js_var = self.cleanup_jsdata(js_record)
        # print(js_var)
        var_key_val = js_var.split("=")
        # print(var_key_val)
        if _JS_VAR_MATCH_TIME_ == var_key_val[0].lower():
            self.extract_matchday(var_key_val[1], euro_odds)

        if var_key_val[0].lower() in self.match_fields:
            euro_odds[var_key_val[0].lower()] = var_key_val[1]

        if var_key_val[0] == _JS_VAR_GAME_:
            self.extract_all_game_odds(var_key_val[1], euro_odds)

        if var_key_val[0] == _JS_VAR_GAME_DETAIL_:
            self.handle_game_detail(var_key_val[1], euro_odds)

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

    def extract_matchday(self, match_datetime, euro_odds):
        # '2017,08-1,11,18,45,00'
        tm = match_datetime.split(',')
        matchday = tm[0] + '-' + tm[1]
        # print(matchday)
        euro_odds[_JS_VAR_MATCH_DAY_] = matchday

    def extract_all_game_odds(self, game, euro_odds):
        vendorlist = self.cleanup_var_game(game)
        # print(vendorlist)
        # print(len(vendorlist))
        for item in vendorlist:
            itemstr = item.encode(_UTF_8_)
            self.build_euroodds(itemstr, euro_odds)

    def build_euroodds(self, oddstr, euro_odds):
        odds_values = oddstr.split('|')
        # print(odds_values[2]) # institue_name
        if odds_values[2] in self.institute_list:
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
            print euro_odds
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
