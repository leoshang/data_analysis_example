
import configparser

_SOFA_SCORE_CONFIG_FILE_ = '/Users/leoshang/workspace/football_data_analysis/sofascore/sofascore/spiders/premier-league.ini'
data_feed_config = configparser.ConfigParser()
data_feed_config.read(_SOFA_SCORE_CONFIG_FILE_)


class SofaScoreConfiguration:

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
    def get_league_name():
        return SofaScoreConfiguration.config_section_map('PremierLeague')['league']

    @staticmethod
    def get_current_season():
        return SofaScoreConfiguration.config_section_map('Season')['current_season']

    @staticmethod
    def get_vote_site():
        return SofaScoreConfiguration.config_section_map('PremierLeague')['vote_site']

    @staticmethod
    def get_season_round_site():
        sofa_season_site = SofaScoreConfiguration.extract_season_link()
        return sofa_season_site + SofaScoreConfiguration.config_section_map('PremierLeague')[
            'season_round_site']

    @staticmethod
    def get_round_link(round_count):
        return SofaScoreConfiguration.get_season_round_site().replace('$round_number', str(round_count))

    @staticmethod
    def extract_season_link():
        sofa_season_id = SofaScoreConfiguration.config_section_map('Season')[SofaScoreConfiguration.get_current_season()]
        sofa_season_site = SofaScoreConfiguration.config_section_map('PremierLeague')['sofa_season_site']
        return sofa_season_site.replace('$season_id', sofa_season_id)
