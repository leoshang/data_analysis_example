# coding=utf-8
import xlsxwriter
import openpyxl
import json

from postgres_odds_analysis.config.configreader import ConfigurationReader
from postgres_odds_analysis.oddsitem import EuroOdds


class WilliamOddsAnalyser(object):
    def __init__(self):
        self.workbook = {}
        league = ConfigurationReader.get_league_name()
        season = ConfigurationReader.get_season()
        analysed_prefix = ConfigurationReader.get_analyse_prefix()
        output_file_name = analysed_prefix + league + season
        self.workbook = xlsxwriter.Workbook('%s.xlsx' % output_file_name)
        self.output_sheet = self.workbook.add_worksheet()
        self.output_sheet.set_default_row(25)
        self.row_count = 0
        self.handicap_map = {u'两球': 2, u'球半/两球': 1.75, u'球半': 1.5, u'一球/球半': 1.25, u'一球': 1, u'半球/一球': 0.75, u'半球': 0.5,
                             u'平手/半球': 0.25, u'平手': 0}
        self.handicap_map_rev = {2: u'两球', 1.75: u'球半/两球', 1.5: u'球半', 1.25: u'一球/球半', 1: u'一球', 0.75: u'半球/一球',
                                 0.5: u'半球', 0.25: u'平手/半球', 0: u'平手'}

    def read_items(self):
        odds_data_file = ConfigurationReader.get_data_file()
        odds_reader = openpyxl.load_workbook(odds_data_file)

        # Get workbook active sheet object
        # from the active attribute
        odds_sheet = odds_reader.active
        return self.process_items(odds_sheet)

    def write_items(self, items):
        self.write_header()
        self.write(items)

    def write_header(self):
        self.output_sheet.write(self.row_count, 0, u'主队')
        self.output_sheet.write(self.row_count, 1, u'客队')
        self.output_sheet.write(self.row_count, 2, u'主队积分')
        self.output_sheet.write(self.row_count, 3, u'客队积分')
        self.output_sheet.write(self.row_count, 4, u'主队排名')
        self.output_sheet.write(self.row_count, 5, u'客队排名')
        self.output_sheet.write(self.row_count, 6, u'主队胜率')
        self.output_sheet.write(self.row_count, 7, u'客队胜率')

        self.output_sheet.write(self.row_count, 8, u'主队近六场赢')
        self.output_sheet.write(self.row_count, 9, u'主队近六场平')
        self.output_sheet.write(self.row_count, 10, u'主队近六场负')

        # visually to keep a empty column 11
        self.output_sheet.write(self.row_count, 12, u'客队近六场赢')
        self.output_sheet.write(self.row_count, 13, u'客队近六场平')
        self.output_sheet.write(self.row_count, 14, u'客队近六场负')

        self.output_sheet.write(self.row_count, 15, u'博彩公司')
        self.output_sheet.write(self.row_count, 17, u'初盘主胜赔付')
        self.output_sheet.write(self.row_count, 18, u'初盘平局赔付')
        self.output_sheet.write(self.row_count, 19, u'初盘客胜赔付')

        self.output_sheet.write(self.row_count, 21, u'初盘主队水位')
        self.output_sheet.write(self.row_count, 22, u'初盘盘口')
        self.output_sheet.write(self.row_count, 23, u'初盘客队水位')

        self.output_sheet.write(self.row_count, 25, u'初盘大球水位')
        self.output_sheet.write(self.row_count, 26, u'初盘进球数')
        self.output_sheet.write(self.row_count, 27, u'初盘小球水位')
        self.row_count += 1

    def process_items(self, odds_sheet):
        handicap_dict = dict()
        for i in range(2, odds_sheet.max_row + 1):
            bookie = odds_sheet.cell(i, 23).value
            handicap = odds_sheet.cell(i, 33).value

            has_handicap = None
            # for h in self.handicap_map.keys():
            #     if handicap == h:
            #         has_handicap = True
            #         break
            if handicap in self.handicap_map:
                # print 'found' + odds_sheet.cell(i, 33).value
                has_handicap = True

            if bookie == 'William Hill' and has_handicap:
                euro_odds = EuroOdds()
                euro_odds['bookie_name_en'] = odds_sheet.cell(i, 23).value
                euro_odds['home_team'] = odds_sheet.cell(i, 6).value
                euro_odds['home_points'] = odds_sheet.cell(i, 8).value
                euro_odds['home_ranking'] = odds_sheet.cell(i, 9).value
                euro_odds['home_win_ratio'] = odds_sheet.cell(i, 10).value
                euro_odds['home_win_of_last_6match'] = odds_sheet.cell(i, 11).value
                euro_odds['home_draw_of_last_6match'] = odds_sheet.cell(i, 12).value
                euro_odds['home_lost_of_last_6match'] = odds_sheet.cell(i, 13).value
                euro_odds['guest_team'] = odds_sheet.cell(i, 14).value
                euro_odds['guest_points'] = odds_sheet.cell(i, 16).value
                euro_odds['guest_ranking'] = odds_sheet.cell(i, 17).value
                euro_odds['guest_win_ratio'] = odds_sheet.cell(i, 18).value
                euro_odds['guest_win_of_last_6match'] = odds_sheet.cell(i, 19).value
                euro_odds['guest_draw_of_last_6match'] = odds_sheet.cell(i, 20).value
                euro_odds['guest_lost_of_last_6match'] = odds_sheet.cell(i, 21).value
                euro_odds['open_home_win'] = odds_sheet.cell(i, 25).value
                euro_odds['open_draw'] = odds_sheet.cell(i, 26).value
                euro_odds['open_guest_win'] = odds_sheet.cell(i, 27).value
                euro_odds['asian_start_home_wager'] = odds_sheet.cell(i, 32).value
                euro_odds['asian_start_handicap'] = self.handicap_map[odds_sheet.cell(i, 33).value]
                euro_odds['asian_start_guest_wager'] = odds_sheet.cell(i, 34).value
                euro_odds['asian_start_more_goal'] = odds_sheet.cell(i, 38).value
                euro_odds['asian_start_goal_total'] = odds_sheet.cell(i, 39).value
                euro_odds['asian_start_less_goal'] = odds_sheet.cell(i, 40).value
                if euro_odds['asian_start_handicap'] in handicap_dict:
                    handicap_dict[euro_odds['asian_start_handicap']].append(euro_odds)
                else:
                    handicap_dict[euro_odds['asian_start_handicap']] = [euro_odds]
        return handicap_dict

    def write(self, handicap_dict):
        self.write_header()
        for key in sorted(handicap_dict):
            for euro_odds in handicap_dict[key]:
                self.do_write(euro_odds)

    def do_write(self, odd):
        handicap = self.handicap_map_rev[odd['asian_start_handicap']]
        self.output_sheet.write(self.row_count, 0, odd['home_team'])
        self.output_sheet.write(self.row_count, 1, odd['guest_team'])
        self.output_sheet.write(self.row_count, 2, odd['home_points'])
        self.output_sheet.write(self.row_count, 3, odd['guest_points'])
        self.output_sheet.write(self.row_count, 4, odd['home_ranking'])
        self.output_sheet.write(self.row_count, 5, odd['guest_ranking'])
        self.output_sheet.write(self.row_count, 6, odd['home_win_ratio'])
        self.output_sheet.write(self.row_count, 7, odd['guest_win_ratio'])
        self.output_sheet.write(self.row_count, 8, odd['home_win_of_last_6match'])
        self.output_sheet.write(self.row_count, 9, odd['home_draw_of_last_6match'])
        self.output_sheet.write(self.row_count, 10, odd['home_lost_of_last_6match'])

        self.output_sheet.write(self.row_count, 12, odd['guest_win_of_last_6match'])
        self.output_sheet.write(self.row_count, 13, odd['guest_draw_of_last_6match'])
        self.output_sheet.write(self.row_count, 14, odd['guest_lost_of_last_6match'])
        self.output_sheet.write(self.row_count, 15, odd['bookie_name_en'])
        self.output_sheet.write(self.row_count, 17, odd['open_home_win'])
        self.output_sheet.write(self.row_count, 18, odd['open_draw'])
        self.output_sheet.write(self.row_count, 19, odd['open_guest_win'])
        self.output_sheet.write(self.row_count, 21, odd['asian_start_home_wager'])
        self.output_sheet.write(self.row_count, 22, handicap)
        self.output_sheet.write(self.row_count, 23, odd['asian_start_guest_wager'])
        self.output_sheet.write(self.row_count, 25, odd['asian_start_more_goal'])
        self.output_sheet.write(self.row_count, 26, odd['asian_start_goal_total'])
        self.output_sheet.write(self.row_count, 27, odd['asian_start_less_goal'])
        self.row_count += 1

    def close_writer(self):
        self.workbook.close()
