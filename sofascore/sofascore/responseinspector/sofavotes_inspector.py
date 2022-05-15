# -*- coding: utf-8 -*-
import json
import scrapy
from datetime import datetime
# from sofascore.responseinspector.sofaround_inspector import SofaRoundInspector
from sofascore.items import SofascoreItem
from sofascore.spiders.sofa_config import SofaScoreConfiguration


class SofaVotesInspector:
    def __init__(self):
        # self.next_round_inspector = SofaRoundInspector()
        pass

    @staticmethod
    def extract_votes(response):
        votes = json.loads(response.body.encode("utf-8"))
        score_item = response.meta.get('score_item')
        score_item['vote_home_win'] = votes['vote']['vote1']
        score_item['vote_draw'] = votes['vote']['voteX']
        score_item['vote_guest_win'] = votes['vote']['vote2']
        yield score_item

