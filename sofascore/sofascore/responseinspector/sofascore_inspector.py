# -*- coding: utf-8 -*-
import json


class SofaScoreInspector:
    def __init__(self):
        pass

    def extract_score(self, response):
        votes = json.loads(response.body.encode("utf-8"))
        score_item = response.meta.get('score_item')
        score_item['vote_home_win'] = votes['vote']['vote1']
        score_item['vote_draw'] = votes['vote']['voteX']
        score_item['vote_guest_win'] = votes['vote']['vote2']
        yield score_item
