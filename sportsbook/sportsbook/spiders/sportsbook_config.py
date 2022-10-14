import configparser

_SPORTSBOOK_CONFIG_FILE_ = '/Users/leoshang/workspace/football_data_analysis/sportsbook/' \
                           'sportsbook/premier-league.ini'

data_feed_config = configparser.ConfigParser()
data_feed_config.read(_SPORTSBOOK_CONFIG_FILE_)


class SportsbookConfiguration:

    def __init__(self, *a, **kw):
        pass

    @staticmethod
    def config_section_map(section):
        dict1 = {}
        options = data_feed_config.options(section)
        for option in options:
            try:
                dict1[option] = data_feed_config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        # print(dict1)
        return dict1

    @staticmethod
    def get_season_round_url():
        return SportsbookConfiguration.config_section_map('League')['season_round_url']

    @staticmethod
    def get_current_round():
        return SportsbookConfiguration.config_section_map('League')['current_round']

    @staticmethod
    def get_round_total():
        return SportsbookConfiguration.config_section_map('League')['round_total']

    @staticmethod
    def get_league():
        return SportsbookConfiguration.config_section_map('League')['league_name']

    @staticmethod
    def get_euro_odds_site():
        return SportsbookConfiguration.config_section_map('League')['euro_odds_site']

    @staticmethod
    def get_asian_odds_site():
        return SportsbookConfiguration.config_section_map('League')['asian_odds_site']

    @staticmethod
    def get_asian_goal_site():
        return SportsbookConfiguration.config_section_map('League')['asian_goal_site']

    @staticmethod
    def get_analysis_site():
        return SportsbookConfiguration.config_section_map('League')['analysis_site']

    @staticmethod
    def get_current_season():
        return SportsbookConfiguration.config_section_map('League')['current_season']

    @staticmethod
    def get_all_asian_links():
        return SportsbookConfiguration.config_section_map('League')['asianoddslink']
