# coding=utf-8
class EuroOdds:
    def __init__(self):
        pass

    @classmethod
    def __set_all__(self, match_id, match_time,
                 bookie_id, bookie_name_en, bookie_name_cn,
                 matchday, season, matchname,
                 hometeam, guestteam,
                 hometeam_cn, guestteam_cn,
                 open_home_win, open_draw, open_guest_win,
                 end_home_win, end_draw, end_guest_win,
                 open_home_prob, open_draw_prob, open_guest_prob,
                 end_home_win_prob, end_draw_prob, end_guest_win_prob):
        self.matchId = match_id
        self.match_time = match_time
        self.bookie_id = bookie_id
        self.bookie_name_en = bookie_name_en
        self.bookie_name_cn = bookie_name_cn

        self.matchday = matchday
        self.season = season
        self.matchname = matchname
        self.hometeam = hometeam
        self.guestteam = guestteam
        self.hometeam_cn = hometeam_cn
        self.guestteam_cn = guestteam_cn

        # 初赔
        self.open_home_win = open_home_win
        self.open_draw = open_draw
        self.open_guest_win = open_guest_win
        # 即时终赔
        self.end_home_win = end_home_win
        self.end_draw = end_draw
        self.end_guest_win = end_guest_win
        # 换算概率
        self.open_home_prob = open_home_prob
        self.open_draw_prob = open_draw_prob
        self.open_guest_prob = open_guest_prob
        self.end_home_win_prob = end_home_win_prob
        self.end_draw_prob = end_draw_prob
        self.end_guest_win_prob = end_guest_win_prob

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return "赛季：{}；比赛日：{}" \
               "比赛: {}; 主队: {}; 客队: {};" \
               "赔率机构Id：{}；赔率机构名称：{}" \
               "初赔主胜: {}; 初赔平局: {}; 初赔客胜: {};" \
               "即时终赔主胜: {}; 即时终赔平局: {}; 即时终赔客胜: {};" \
               "初赔主胜（换算）概率: {}; " \
               "初赔平局（换算）概率: {}; " \
               "初赔客胜（换算）概率: {};" \
               "终赔主胜（换算）概率: {}; " \
               "终赔平局（换算）概率: {}; " \
               "终赔客胜（换算）概率: {}".format(
                self.season, self.matchday,
                self.matchname, self.hometeam_cn, self.guestteam_cn,
                self.bookie_id, self.bookie_name_cn,
                self.open_home_win, self.open_draw, self.open_guest_win,
                self.end_home_win, self.end_draw, self.end_guest_win,
                self.open_home_prob, self.open_draw_prob, self.open_guest_prob,
                self.end_home_win_prob, self.end_draw_prob, self.end_guest_win_prob)
