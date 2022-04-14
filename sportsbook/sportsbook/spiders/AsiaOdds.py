class AsiaOdds:
    def __init__(self, matchtime, handicap_goal, home_waterlevel, guest_waterlevel):
        self.matchtime = matchtime
        self.handicap_goal = handicap_goal
        self.home_waterlevel = home_waterlevel
        self.guest_waterlevel = guest_waterlevel

    def __str__(self):
        return "matchtime: {}; " \
               "handicap_goal: {}; " \
               "home water level: {}; " \
               "guest water level: {}.".format(self.matchtime, self.handicap_goal,
                                               self.home_waterlevel, self.guest_waterlevel)

