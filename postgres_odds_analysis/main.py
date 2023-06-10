# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from postgres_odds_analysis.analyse.williamhillanalyser import WilliamOddsAnalyser
from postgres_odds_analysis.config.configreader import ConfigurationReader


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press ⌘F8 to toggle the breakpoint.

# based on team's latest six games!
def cal_team_recent_form(lst):
    weights = [1, 1, 1, 1.4, 1.7, 2]
    values = {'w': 3, 'd': 1, 'l': 0}

    total_sum = 0
    current_sum = 0
    current_char = None

    for i, char in enumerate(lst):
        if char == current_char:
            current_sum += values[char]
        else:
            if current_char is not None:
                total_sum += current_sum * weights[i - 1]
            current_char = char
            current_sum = values[char]

    total_sum += current_sum * weights[-1]

    return total_sum


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # datafile = ConfigurationReader.get_data_file()
    # print_hi(datafile)
    # print_hi(ConfigurationReader.get_season())
    # william_analyser = WilliamOddsAnalyser()
    # handicap_dict = william_analyser.read_items()
    # william_analyser.write(handicap_dict)
    # william_analyser.close_writer()
    result = cal_team_recent_form(['w', 'd', 'l', 'w', 'd', 'l'])
    print(result)  # Output: 9.9

    result = cal_team_recent_form(['l', 'l', 'd', 'd', 'w', 'w'])
    print(result)  # Output: 14.8

    result = cal_team_recent_form(['d', 'd', 'l', 'l', 'w', 'w'])
    print(result)  # Output: 14.0

    result = cal_team_recent_form(['w', 'w', 'd', 'd', 'l', 'l'])
    print(result)  # Output: 8.8

    result = cal_team_recent_form(['w', 'w', 'l', 'l', 'd', 'd'])
    print(result)  # Output: 10.8

    result = cal_team_recent_form(['d', 'd', 'l', 'w', 'w', 'w'])
    print(result)  # Output: 20.0


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
