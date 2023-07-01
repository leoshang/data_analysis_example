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


def calculate_occurrences(number_groups):
    number_occurrence = {}
    for group in number_groups:
        for n in list(group):
            if n in number_occurrence:
                number_occurrence[n] += 1
            else:
                number_occurrence[n] = 1
    return number_occurrence


def calculate_sum_of_occurrences(number_groups):
    number_occurrence = calculate_occurrences(number_groups)
    sums = {}
    for group in number_groups:
        occurrence_sum = 0
        g_key = ""
        for n in list(group):
            occurrence_sum += number_occurrence[n]
            g_key += str(n) + "-"
        sums[g_key[:-1]] = occurrence_sum
    return sums


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

    # test lotto
    groups = [
        [6, 21, 23, 26, 43],
        [6, 12, 36, 37, 44],
        [10, 11, 31, 37, 44],
        [1, 15, 19, 24, 33],
        [16, 28, 32, 36, 48],
        [5, 19, 33, 37, 42],
        [7, 11, 20, 21, 29],
        [16, 28, 31, 35, 42],
        [5, 13, 16, 41, 45],
        [12, 21, 24, 28, 40],
        [4, 8, 9, 30, 35],
        [11, 12, 13, 23, 26],
        [17, 18, 30, 33, 35],
        [6, 11, 29, 34, 39],
        [10, 27, 30, 32, 34],
        [28, 30, 31, 45, 46],
        [1, 5, 8, 20, 35],
        [1, 2, 11, 14, 36],
        [1, 3, 29, 45, 47],
        [2, 8, 16, 21, 39],
        [8, 9, 11, 13, 50],
        [5, 7, 21, 22, 29],
        [8, 13, 24, 35, 46],
        [11, 29, 32, 46, 47],
        [5, 19, 33, 36, 42]
    ]

    special_numbers = [
        [3, 9],
        [1, 11],
        [5, 12],
        [7, 8],
        [5, 10],
        [7, 9],
        [6, 11],
        [2, 10],
        [3, 6],
        [1, 3],
        [6, 7],
        [11, 12],
        [6, 8],
        [2, 3],
        [5, 8],
        [4, 8],
        [3, 12],
        [2, 3],
        [5, 8],
        [4, 5],
        [6, 11],
        [3, 10],
        [6, 8],
        [5, 7],
        [7, 12]
    ]

    #occurrences = calculate_occurrences(groups)

    # Print the occurrences in descending order
    #print("Number : Occurrences")
    #for number, occurrence in sorted(occurrences.items(), key=lambda x: x[1], reverse=True):
    #    print(str(number) + " :   " + str(occurrence))
#
    #sum_occurrence = calculate_sum_of_occurrences(groups)

    #print("group : Sum of Occurrences")
    #for number, occurrence in sorted(sum_occurrence.items(), key=lambda x: x[1], reverse=True):
    #    print(str(number) + " :   " + str(occurrence))

    print("Special Number : Occurrences")
    occurrences = calculate_occurrences(special_numbers)
    for number, occurrence in sorted(occurrences.items(), key=lambda x: x[1], reverse=True):
        print(str(number) + " :   " + str(occurrence))

    print("group : Sum of Occurrences")
    sum_occurrence = calculate_sum_of_occurrences(special_numbers)
    for number, occurrence in sorted(sum_occurrence.items(), key=lambda x: x[1], reverse=True):
        print(str(number) + " :   " + str(occurrence))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
