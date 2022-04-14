class MatchEuroOdds:
    def __init__(self):
        self.matchday = None
        self.institution_name = None
        self.institution_id = None
        self.matchname = None
        self.hometeam = None
        self.guestteam = None
        self.season = None
        self.euro_odds_list = []

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return str(self.__dict__)

    def add_euro_odds(self, odds):
        self.euro_odds_list.append(odds)

