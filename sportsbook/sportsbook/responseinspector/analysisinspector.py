# -*- coding: utf-8 -*-

_UTF_8_ = "utf-8"


# 第一轮的数据可以省略因为是上个赛季的！！！
class AnalysisInspector:
    def __init__(self):
        self.home_table_bgcolor = "//table[@bgcolor='#E6CF9F'][1]"
        self.guest_table_bgcolor = "//table[@bgcolor='#B0D2E3'][1]"
        self.first_table = "/table[1]"
        self.first_row = "/tr[1]"
        self.second_row = "/tr[2]"
        self.third_row = "/tr[3]"
        self.sixth_row = "/tr[6]"
        self.first_column = "/td[1]"
        self.second_column = "/td[2]"
        self.third_column = "/td[3]"
        self.fourth_column = "/td[4]"
        self.fifth_column = "/td[5]"
        self.ninth_column = "/td[9]"
        self.tenth_column = "/td[10]"
        self.eleventh_column = "/td[11]"
        self.text_val = "/text()"
        self.node_keymap = {}
        pass

    def init_xpath(self, response):
        if response.xpath("//div[@id='porlet_5']").get():
            home_table = "//div[@id='porlet_5']" + "/" + self.first_table + "/" + self.first_row + self.first_column \
                         + "/" + self.first_table
            guest_table = "//div[@id='porlet_5']" + "/" + self.first_table + "/" + self.first_row + self.second_column \
                          + "/" + self.first_table
            home_total_row = home_table + "/" + self.third_row
            guest_total_row = guest_table + "/" + self.third_row
        else:
            home_table = self.home_table_bgcolor
            guest_table = self.guest_table_bgcolor
            home_total_row = home_table + self.third_row
            guest_total_row = guest_table + self.third_row

        home_last_6match_row = home_table + self.sixth_row
        guest_last_6match_row = guest_table + self.sixth_row
        # 主队的积分，排名，胜率，近六场的胜平负
        home_points = home_total_row + self.ninth_column + self.text_val
        guest_points = guest_total_row + self.ninth_column + self.text_val

        home_ranking = home_total_row + self.tenth_column + self.text_val
        guest_ranking = guest_total_row + self.tenth_column + self.text_val

        home_win_ratio = home_total_row + self.eleventh_column + self.text_val
        guest_win_ratio = guest_total_row + self.eleventh_column + self.text_val

        home_win_of_last_6match = home_last_6match_row + self.third_column + self.text_val
        home_draw_of_last_6match = home_last_6match_row + self.fourth_column + self.text_val
        home_lost_of_last_6match = home_last_6match_row + self.fifth_column + self.text_val

        # 客队的积分，排名，胜率，近六场的胜平负
        guest_win_of_last_6match = guest_last_6match_row + self.third_column + self.text_val
        guest_draw_of_last_6match = guest_last_6match_row + self.fourth_column + self.text_val
        guest_lost_of_last_6match = guest_last_6match_row + self.fifth_column + self.text_val

        self.node_keymap[home_points] = "home_points"
        self.node_keymap[home_ranking] = "home_ranking"
        self.node_keymap[home_win_ratio] = "home_win_ratio"
        self.node_keymap[home_win_of_last_6match] = "home_win_of_last_6match"
        self.node_keymap[home_draw_of_last_6match] = "home_draw_of_last_6match"
        self.node_keymap[home_lost_of_last_6match] = "home_lost_of_last_6match"
        self.node_keymap[guest_points] = "guest_points"
        self.node_keymap[guest_ranking] = "guest_ranking"
        self.node_keymap[guest_win_ratio] = "guest_win_ratio"
        self.node_keymap[guest_win_of_last_6match] = "guest_win_of_last_6match"
        self.node_keymap[guest_draw_of_last_6match] = "guest_draw_of_last_6match"
        self.node_keymap[guest_lost_of_last_6match] = "guest_lost_of_last_6match"
        return [home_points, home_ranking, home_win_ratio,
                home_win_of_last_6match, home_draw_of_last_6match, home_lost_of_last_6match,
                guest_points, guest_ranking, guest_win_ratio,
                guest_win_of_last_6match, guest_draw_of_last_6match, guest_lost_of_last_6match]

    def extract(self, response):
        odds_array = response.meta.get("odds_array")
        season = odds_array[0]['season'].split('-')[0]
        target_html_nodes = self.init_xpath(response)
        analysis = {}
        for node in target_html_nodes:
            # print node
            node_element = response.xpath(node).get()
            if node_element:
                node_value = node_element.encode(_UTF_8_)
            else:
                print node
                node_value = -1
            analysis[self.node_keymap[node]] = node_value
        for x in odds_array:
            # append asian_odds into euro_odds
            x.update(analysis)
            yield x
        pass
