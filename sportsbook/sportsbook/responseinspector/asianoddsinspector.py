# -*- coding: utf-8 -*-
from html5lib import html5parser
from sportsbook.responseinspector.asiangoalinspector import AsianGoalsInspector

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
        self.SCORE_PATH_ID = "//div[@id='headVs']"
        self.HOME_SCORE = self.SCORE_PATH_ID + "//div[@class='score'][1]/text()"
        self.GUEST_SCORE = self.SCORE_PATH_ID + "//div[@class='score'][2]/text()"
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
        self.asian_odds_fields = {self.HOME_SCORE: "home_score",
                                  self.GUEST_SCORE: "guest_score",
                                  self.MATCH_TIME_PATH: "match_time",
                                  self.ODDS_BOOKIE_PATH: "asian_bookie",
                                  self.START_HOME_WAGER_PATH: "asian_start_homewager",
                                  self.START_HANDICAP_PATH: "asian_start_handicap",
                                  self.START_GUEST_WAGER_PATH: "asian_start_guestwager",
                                  self.END_HOME_WAGER_PATH: "asian_end_homewager",
                                  self.END_HANDICAP_PATH: "asian_end_handicap",
                                  self.END_GUEST_WAGER_PATH: "asian_end_guestwager"}

        self.target_html_nodes = [self.HOME_SCORE, self.GUEST_SCORE, self.MATCH_TIME_PATH, self.ODDS_BOOKIE_PATH,
                                  self.START_HOME_WAGER_PATH, self.START_HANDICAP_PATH, self.START_GUEST_WAGER_PATH,
                                  self.END_HOME_WAGER_PATH, self.END_HANDICAP_PATH, self.END_GUEST_WAGER_PATH]
        self.asian_goal_inspector = AsianGoalsInspector()
        pass

    def handle_asian_odds(self, response):
        asian_odds = {}
        for node in self.target_html_nodes:
            node_text = response.xpath(node).get()
            if node_text:
                node_value = node_text.encode(_UTF_8_)
                asian_odds[self.asian_odds_fields[node]] = node_value
        return asian_odds

    def extract_asian_odds(self, response):
        # all_odds = response.text.encode(_UTF_8_)
        asian_odds = {}
        for node in self.target_html_nodes:
            node_text = response.xpath(node).get()
            if node_text:
                node_value = node_text.encode(_UTF_8_)
                asian_odds[self.asian_odds_fields[node]] = node_value
        # print asian_odds
        odds_array = response.meta.get("euro_odds_array")
        asian_goal_link = response.meta.get("asian_goal_link")
        analysis_link = response.meta.get("analysis_link")
        scrapy_instance = response.meta.get("scrapy_instance")
        for x in odds_array:
            # append asian_odds into euro_odds
            x.update(asian_odds)

        request_goal = scrapy_instance.Request(asian_goal_link,
                                               callback=self.asian_goal_inspector.extract_asian_goal,
                                               meta={'odds_array': odds_array,
                                                     'analysis_link': analysis_link,
                                                     'scrapy_instance': scrapy_instance
                                                     })
        request_goal = request_goal.replace(encoding='gb18030')
        yield request_goal

    pass
