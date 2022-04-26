# -*- coding: utf-8 -*-
_UTF_8_ = "utf-8"

# div id="webmain"
# 	table id="odds"
# 		tbody
# 			the 3. tr is 澳门
# 						1. <td>
# 							澳门
# 						   </td>
# 						3. <td> 初盘主队水位
# 						4. 初盘盘口
# 						5. 初盘客队水位
# 						8. 即时主队水位
# 						9. 即时盘口
# 						10.即时客队水位
ODDS_TABLE_ID = "//table[@id='odds']"
TARGET_SECTION_PATH = "tr[2]/text()"  # index starts from 0
ODD_BOOKIE_PATH = "td[0]/text()"
START_HOME_WAGER_PATH = "td[2]/text()"
START_HANDICAP_PATH = "td[3]/text()"
START_GUEST_WAGER_PATH = "td[4]/text()"
END_HOME_WAGER_PATH = "td[7]/text()"
END_HANDICAP_PATH = "td[8]/text()"
END_GUEST_WAGER_PATH = "td[8]/text()"


class AsianOddsInspector:
    def __init__(self):
        pass

    def parse(self, response):
        odds_table = response.xpath(self.ODDS_TABLE_ID)

    def extract_asian_odds(self, response):
        all_odds = response.text.encode(_UTF_8_)

    pass
