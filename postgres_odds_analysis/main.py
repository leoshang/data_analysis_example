# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from postgres_odds_analysis.analyse.williamhillanalyser import WilliamOddsAnalyser
from postgres_odds_analysis.config.configreader import ConfigurationReader


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    datafile = ConfigurationReader.get_data_file()
    print_hi(datafile)
    print_hi(ConfigurationReader.get_season())
    william_analyser = WilliamOddsAnalyser()
    handicap_dict = william_analyser.read_items()
    william_analyser.write(handicap_dict)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
