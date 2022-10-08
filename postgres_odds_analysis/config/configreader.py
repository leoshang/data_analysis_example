import configparser

_CONFIG_FILE_ = '/Users/leoshang/workspace/football_data_analysis/postgres_odds_analysis/config/william-premierleague.ini'

data_feed_config = configparser.ConfigParser()
data_feed_config.read(_CONFIG_FILE_)


class ConfigurationReader:

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
    def get_location():
        return ConfigurationReader.config_section_map('League')['location']

    @staticmethod
    def get_league_name():
        return ConfigurationReader.config_section_map('League')['name']

    @staticmethod
    def get_season():
        return ConfigurationReader.config_section_map('League')['season']

    @staticmethod
    def get_suffix():
        return ConfigurationReader.config_section_map('League')['suffix']

    @staticmethod
    def get_data_file():
        return ConfigurationReader.get_location() + ConfigurationReader.get_league_name() + \
               ConfigurationReader.get_season() + ConfigurationReader.get_suffix()

