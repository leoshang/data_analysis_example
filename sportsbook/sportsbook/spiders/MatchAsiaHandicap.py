class MatchAsiaHandicap:
    def __init__(self, matchday, institution_name, institution_id, matchname, hometeam, guestteam):
        self.matchday = matchday
        self.institution_name = institution_name
        self.institution_id = institution_id
        self.matchname = matchname
        self.hometeam = hometeam
        self.guestteam = guestteam
        self.handicap_items = []

    def add_handicap_odds(self, asia_odds):
        self.handicap_items.append(asia_odds)
