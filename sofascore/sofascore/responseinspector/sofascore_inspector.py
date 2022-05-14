# -*- coding: utf-8 -*-
# from sportsbook.responseinspector.eurooddsInspector import EuroOddsInspector
import json


class SofaScoreInspector:
    def __init__(self):
        pass

    def extract_score(self, response):
        votes = json.loads(response.body.encode("utf-8"))
        print votes['vote']['vote1']
        print votes['vote']['vote2']
        print votes['vote']['voteX']
        pass
