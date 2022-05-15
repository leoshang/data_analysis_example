# -*- coding: utf-8 -*-
from __future__ import division
import scrapy

import json
from datetime import datetime

from sofascore.items import SofascoreItem
from sofascore.responseinspector.sofavotes_inspector import SofaVotesInspector
from sofascore.spiders.sofa_config import SofaScoreConfiguration

_UTF_8_ = "utf-8"


class SofaScoreCrawler(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "sofascorespider"
    allowed_domains = ["sofascore.com"]

    def __init__(self, *a, **kw):
        super(SofaScoreCrawler, self).__init__(*a, **kw)
        self.start_urls = []
        self.votes_inspector = SofaVotesInspector()
        self.round_count = 1

        round_link = SofaScoreConfiguration.get_round_link(self.round_count)
        self.start_urls.append(round_link)
        print(self.start_urls)

    def parse(self, response):
        # print response.request.headers['User-Agent']
        # print response.request.headers.get('Referrer', None)
        print response.url
        all_match_data = json.loads(response.body.encode(_UTF_8_))
        data1_array = all_match_data['events']

        for match in data1_array:
            score_item = SofascoreItem()
            score_item['match_id'] = match['id']
            score_item['startTimestamp'] = datetime.utcfromtimestamp(match['startTimestamp']).strftime('%Y-%m-%d %H:%M:%S')
            score_item['hometeam'] = match['homeTeam']['name']
            score_item['hometeam_fans'] = match['homeTeam']['userCount']
            score_item['hometeam_score'] = match['homeScore']['normaltime']

            score_item['guestteam'] = match['awayTeam']['name']
            score_item['guestteam_fans'] = match['awayTeam']['userCount']
            score_item['guestteam_score'] = match['awayScore']['normaltime']

            match_vote_url = SofaScoreConfiguration.get_vote_site().replace('$event_id', str(match['id']))
            print match_vote_url

            self.round_count += 1
            next_round_url = SofaScoreConfiguration.get_season_round_site().replace('$round_number',
                                                                                    str(self.round_count))

            request_event = scrapy.Request(match_vote_url, callback=self.votes_inspector.extract_votes,
                                           meta={'score_item': score_item,
                                                 'next_round': self.round_count,
                                                 'next_round_url': next_round_url})
            yield request_event

