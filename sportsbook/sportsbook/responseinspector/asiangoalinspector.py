# -*- coding: utf-8 -*-
from sportsbook.responseinspector.analysisinspector import AnalysisInspector

_UTF_8_ = "utf-8"


class AsianGoalsInspector:
    def __init__(self):
        self.ODDS_TABLE_ID = "//table[@id='odds']"
        self.TARGET_SECTION_PATH = self.ODDS_TABLE_ID + "//tr[3]"  # index starts from 1
        self.START_MORE_GOAL_WAGER = self.TARGET_SECTION_PATH + "/td[3]/text()"
        self.START_GOAL_TOTAL = self.TARGET_SECTION_PATH + "/td[4]/text()"
        self.START_LESS_GOAL_WAGER = self.TARGET_SECTION_PATH + "/td[5]/text()"
        self.END_MORE_GOAL_WAGER = self.TARGET_SECTION_PATH + "/td[9]/text()"
        self.END_GOAL_TOTAL = self.TARGET_SECTION_PATH + "/td[10]/text()"
        self.END_LESS_GOAL_WAGER = self.TARGET_SECTION_PATH + "/td[11]/text()"
        self.asian_goals_fields = {
            self.START_MORE_GOAL_WAGER: "asian_start_more_goal",
            self.START_GOAL_TOTAL: "asian_start_goal_total",
            self.START_LESS_GOAL_WAGER: "asian_start_less_goal",
            self.END_MORE_GOAL_WAGER: "asian_end_more_goal",
            self.END_GOAL_TOTAL: "asian_end_goal_total",
            self.END_LESS_GOAL_WAGER: "asian_end_less_goal"
        }

        self.target_html_nodes = [self.START_MORE_GOAL_WAGER, self.START_GOAL_TOTAL, self.START_LESS_GOAL_WAGER,
                                  self.END_MORE_GOAL_WAGER, self.END_GOAL_TOTAL, self.END_LESS_GOAL_WAGER]
        self.analysis_inspector = AnalysisInspector()
        pass

    def extract_asian_goal(self, response):
        # all_odds = response.text.encode(_UTF_8_)
        asian_goals = {}
        for node in self.target_html_nodes:
            node_text = response.xpath(node).get()
            if node_text:
                node_value = node_text.encode(_UTF_8_)
                asian_goals[self.asian_goals_fields[node]] = node_value
        # print asian_goals
        odds_array = response.meta.get("odds_array")
        analysis_link = response.meta.get("analysis_link")
        scrapy_instance = response.meta.get("scrapy_instance")
        for x in odds_array:
            # append asian_goals into euro_odds
            x.update(asian_goals)

        request_analysis = scrapy_instance.Request(analysis_link,
                                                   callback=self.analysis_inspector.extract,
                                                   meta={'odds_array': odds_array})
        yield request_analysis

    pass
