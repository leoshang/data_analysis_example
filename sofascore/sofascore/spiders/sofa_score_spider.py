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

        for round_count in range(1, 39):
            round_link = SofaScoreConfiguration.get_round_link(round_count)
            self.start_urls.append(round_link)
        # print(self.start_urls)

    def parse(self, response):
        # print response.request.headers['User-Agent']
        # print response.request.headers.get('Referrer', None)

        all_match_data = json.loads(response.body.encode(_UTF_8_))
        data1_array = all_match_data['events']

        for match in data1_array:
            score_item = SofascoreItem()
            # print json.dumps(match)
            score_item['round'] = match['roundInfo']['round']
            score_item['match_id'] = match['id']
            score_item['startTimestamp'] = datetime.utcfromtimestamp(match['startTimestamp']).strftime('%Y-%m-%d %H:%M:%S')
            score_item['hometeam'] = match['homeTeam']['name']
            score_item['hometeam_fans'] = match['homeTeam']['userCount']
            # print match['tournament']['name']
            # print match['slug']
            if match['homeScore']:
                score_item['hometeam_score'] = match['homeScore']['normaltime']
            else:
                print str(match['id']) + ':' + str(match['roundInfo']['round'])\
                      + ':' + match['homeTeam']['name'] + ':' + match['awayTeam']['name']
            if match['awayScore']:
                score_item['guestteam_score'] = match['awayScore']['normaltime']

            score_item['guestteam'] = match['awayTeam']['name']
            score_item['guestteam_fans'] = match['awayTeam']['userCount']

            match_vote_url = SofaScoreConfiguration.get_vote_site().replace('$event_id', str(match['id']))
            # print 'vote url: ' + match_vote_url

            request_event = scrapy.Request(match_vote_url, callback=SofaVotesInspector.extract_votes,
                                           meta={'score_item': score_item})
            yield request_event

