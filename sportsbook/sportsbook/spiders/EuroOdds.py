class EuroOdds:
    def __init__(self, matchtime, odds_home_win, odds_draw, odds_guest_win, home_prob=0, draw_prob=0, guest_prob=0):
        self.matchtime = matchtime
        self.home_win = odds_home_win
        self.draw = odds_draw
        self.guest_win = odds_guest_win
        self.home_prob = home_prob
        self.draw_prob = draw_prob
        self.guest_prob = guest_prob
        self.euro_asia_odds_mapping = {}

    def __str__(self):
        return "home_win: {}; draw: {}; guest_win: {};" \
               "home probability: {}; " \
               "draw probability: {}; "\
               "guest probability: {};" \
               "odds conversion: {}".format(self.home_win, self.draw, self.guest_win,
                                                   self.home_prob, self.draw_prob, self.guest_prob,
                                                   self.euro_asia_odds_mapping)
