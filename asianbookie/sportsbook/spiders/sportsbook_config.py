import configparser

_SPORTSBOOK_CONFIG_FILE_ = '/Users/leoshang/workspace/football_data_analysis/asianbookie/' \
                           'sportsbook/spiders/premier-league.ini'

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
    def get_league():
        return SportsbookConfiguration.config_section_map('League')['league_name']

    @staticmethod
    def get_current_season():
        return SportsbookConfiguration.config_section_map('League')['current_season']

    @staticmethod
    def get_all_asian_links():
        return SportsbookConfiguration.config_section_map('League')['asianoddslink']

    @staticmethod
    def get_bookiename():
        return SportsbookConfiguration.config_section_map('League')['bookie_name']

    @staticmethod
    def get_match_js_url():
        return SportsbookConfiguration.config_section_map('League')['match_js_url']
