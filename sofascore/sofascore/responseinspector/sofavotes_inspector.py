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

    def extract_votes(self, response):
        next_round_url = response.meta.get('next_round_url')
        next_round = response.meta.get('next_round')
        votes = json.loads(response.body.encode("utf-8"))
        score_item = response.meta.get('score_item')
        score_item['vote_home_win'] = votes['vote']['vote1']
        score_item['vote_draw'] = votes['vote']['voteX']
        score_item['vote_guest_win'] = votes['vote']['vote2']
        yield score_item
        request_next_round = scrapy.Request(next_round_url, callback=self.extract_all_matches,
                                            meta={'next_round': next_round})
        yield request_next_round

    def extract_all_matches(self, response):
        current_round = response.meta.get('next_round')
        all_match_data = json.loads(response.body.encode('utf-8'))
        data1_array = all_match_data['events']

        for match in data1_array:
            score_item = SofascoreItem()
            score_item['match_id'] = match['id']
            score_item['startTimestamp'] = datetime.utcfromtimestamp(match['startTimestamp']).strftime(
                '%Y-%m-%d %H:%M:%S')
            score_item['hometeam'] = match['homeTeam']['name']
            score_item['hometeam_fans'] = match['homeTeam']['userCount']
            score_item['hometeam_score'] = match['homeScore']['normaltime']

            score_item['guestteam'] = match['awayTeam']['name']
            score_item['guestteam_fans'] = match['awayTeam']['userCount']
            score_item['guestteam_score'] = match['awayScore']['normaltime']

            match_vote_url = SofaScoreConfiguration.get_vote_site().replace('$event_id', str(match['id']))
            print match_vote_url

            next_round = current_round + 1
            next_round_url = SofaScoreConfiguration.get_season_round_site().replace('$round_number', str(next_round))

            request_event = scrapy.Request(match_vote_url, callback=self.extract_votes,
                                           meta={'score_item': score_item,
                                                 'next_round': next_round,
                                                 'next_round_url': next_round_url})
            yield request_event
