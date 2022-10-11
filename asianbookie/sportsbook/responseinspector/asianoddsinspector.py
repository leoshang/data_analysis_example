# -*- coding: utf-8 -*-
from html5lib import html5parser

from asianbookie.sportsbook.items import AsianOdds

_UTF_8_ = "utf-8"

# div id="webmain"
# 	table id="odds"
# 		tbody
# 			the 第三个tr：tr[3] is 澳门
# 						1. <td>
# 							澳门
# 						   </td>
# 						3. <td> 初盘主队水位
# 						4. 初盘盘口
# 						5. 初盘客队水位
# 						9. 即时主队水位
# 						10. 即时盘口
# 						11.即时客队水位


class AsianOddsInspector:
    def __init__(self):
        self.MATCH_TIME_PATH = "//div[@class='vs']/div[@class='row']/a/following-sibling::text()"
        self.ODDS_TABLE_ID = "//table[@id='odds']"
        self.TARGET_SECTION_PATH = self.ODDS_TABLE_ID + "//tr[3]"  # index starts from 1
        self.ODDS_BOOKIE_PATH = self.TARGET_SECTION_PATH + "/td[1]/text()"
        self.START_HOME_WAGER_PATH = self.TARGET_SECTION_PATH + "/td[3]/text()"
        self.START_HANDICAP_PATH = self.TARGET_SECTION_PATH + "/td[4]/text()"
        self.START_GUEST_WAGER_PATH = self.TARGET_SECTION_PATH + "/td[5]/text()"
        self.END_HOME_WAGER_PATH = self.TARGET_SECTION_PATH + "/td[9]/text()"
        self.END_HANDICAP_PATH = self.TARGET_SECTION_PATH + "/td[10]/text()"
        self.END_GUEST_WAGER_PATH = self.TARGET_SECTION_PATH + "/td[11]/text()"
        self.asian_odds_fields = {self.START_HOME_WAGER_PATH: "asian_start_homewager",
                                  self.START_HANDICAP_PATH: "asian_start_handicap",
                                  self.START_GUEST_WAGER_PATH: "asian_start_guestwager",
                                  self.END_HOME_WAGER_PATH: "asian_end_homewager",
                                  self.END_HANDICAP_PATH: "asian_end_handicap",
                                  self.END_GUEST_WAGER_PATH: "asian_end_guestwager"}

        self.target_html_nodes = [self.START_HOME_WAGER_PATH, self.START_HANDICAP_PATH, self.START_GUEST_WAGER_PATH,
                                  self.END_HOME_WAGER_PATH, self.END_HANDICAP_PATH, self.END_GUEST_WAGER_PATH]
        pass

    def handle_asian_odd(self, response):
        asian_odd_item = AsianOdds()
        if response.encoding == 'cp1252':
            response = response.encoding('cp1252')
        for node in self.target_html_nodes:
            node_text = response.xpath(node).get()
            if node_text:
                node_value = node_text.encode(_UTF_8_)
                asian_odd_item[self.asian_odds_fields[node]] = node_value
        return asian_odd_item
    pass
