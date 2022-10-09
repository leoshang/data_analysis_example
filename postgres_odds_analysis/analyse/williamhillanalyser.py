# coding=utf-8
import xlsxwriter
import openpyxl
import json

from postgres_odds_analysis.config.configreader import ConfigurationReader
from postgres_odds_analysis.oddsitem import EuroOdds


class WilliamOddsAnalyser(object):
    def __init__(self):
        self.workbook = {}
        self.output_sheet = {}
        self.row_count = 0
        self.handicap_map = {u'两球': 2, u'球半/两球': 1.75, u'球半': 1.5, u'一球/球半': 1.25, u'一球': 1, u'半球/一球': 0.75, u'半球': 0.5,
                             u'平手/半球': 0.25, u'平手': 0}
        self.handicap_map_rev = {2: '两球', 1.75: '球半/两球', 1.5: '球半', 1.25: '一球/球半', 1: '一球', 0.75: '半球/一球', 0.5: '半球',
                                 0.25: '平手/半球', 0: '平手'}

    def read_items(self):
        odds_data_file = ConfigurationReader.get_data_file()
        odds_reader = openpyxl.load_workbook(odds_data_file)

        # Get workbook active sheet object
        # from the active attribute
        odds_sheet = odds_reader.active
        return self.process_items(odds_sheet)

    def write_items(self, items):
        league = ConfigurationReader.get_league_name()
        season = ConfigurationReader.get_season()
        analysed_prefix = ConfigurationReader.get_analyse_prefix()
        self.workbook = xlsxwriter.Workbook('%s.xlsx' % analysed_prefix + league + season)
        self.output_sheet = self.workbook.add_worksheet()
        self.output_sheet.set_default_row(25)
        self.write_header()
        self.write(items)

    def write_header(self):
        self.output_sheet.write(self.row_count, 1, '主队'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 2, '主队积分'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 3, '主队排名'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 4, '主队胜率'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 5, '主队近六场赢'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 6, '主队近六场平'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 7, '主队近六场负'.encode('utf-8'))

        self.output_sheet.write(self.row_count, 8, '客队'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 9, '客队积分'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 10, '客队排名'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 11, '客队胜率'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 12, '客队近六场赢'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 13, '客队近六场平'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 14, '客队近六场负'.encode('utf-8'))

        self.output_sheet.write(self.row_count, 15, '博彩公司'.encode('utf-8'))

        self.output_sheet.write(self.row_count, 16, '初盘主胜赔付'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 17, '初盘平局赔付'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 18, '初盘客胜赔付'.encode('utf-8'))

        self.output_sheet.write(self.row_count, 19, '初盘主队水位'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 20, '初盘盘口'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 21, '初盘客队水位'.encode('utf-8'))

        self.output_sheet.write(self.row_count, 22, '初盘大球水位'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 23, '初盘进球数'.encode('utf-8'))
        self.output_sheet.write(self.row_count, 24, '初盘小球水位'.encode('utf-8'))
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
        for key in sorted(handicap_dict):
            for euro_odds in handicap_dict[key]:
                if len(euro_odds) == 1:
                    self.do_write(euro_odds)
                else:
                    for odd in euro_odds:
                        self.do_write(odd)

    def do_write(self, euro_odds):
        self.output_sheet.write(self.row_count, 1, euro_odds['home_team'])
        self.output_sheet.write(self.row_count, 2, euro_odds['home_points'])
        self.output_sheet.write(self.row_count, 3, euro_odds['home_ranking'])
        self.output_sheet.write(self.row_count, 4, euro_odds['home_win_ratio'])
        self.output_sheet.write(self.row_count, 5, euro_odds['home_win_of_last_6match'])
        self.output_sheet.write(self.row_count, 6, euro_odds['home_draw_of_last_6match'])
        self.output_sheet.write(self.row_count, 7, euro_odds['home_lost_of_last_6match'])
        self.output_sheet.write(self.row_count, 8, euro_odds['guest_team'])
        self.output_sheet.write(self.row_count, 9, euro_odds['guest_points'])
        self.output_sheet.write(self.row_count, 10, euro_odds['guest_ranking'])
        self.output_sheet.write(self.row_count, 11, euro_odds['guest_win_ratio'])
        self.output_sheet.write(self.row_count, 12, euro_odds['guest_win_of_last_6match'])
        self.output_sheet.write(self.row_count, 13, euro_odds['guest_draw_of_last_6match'])
        self.output_sheet.write(self.row_count, 14, euro_odds['guest_lost_of_last_6match'])
        self.output_sheet.write(self.row_count, 15, euro_odds['bookie_name_en'])
        self.output_sheet.write(self.row_count, 16, euro_odds['open_home_win'])
        self.output_sheet.write(self.row_count, 17, euro_odds['open_draw'])
        self.output_sheet.write(self.row_count, 18, euro_odds['open_guest_win'])
        self.output_sheet.write(self.row_count, 19, euro_odds['asian_start_home_wager'])
        self.output_sheet.write(self.row_count, 20, euro_odds['asian_start_handicap'])
        self.output_sheet.write(self.row_count, 21, euro_odds['asian_start_guest_wager'])
        self.output_sheet.write(self.row_count, 22, euro_odds['asian_start_more_goal'])
        self.output_sheet.write(self.row_count, 23, euro_odds['asian_start_goal_total'])
        self.output_sheet.write(self.row_count, 24, euro_odds['asian_start_less_goal'])
        self.row_count += 1

    def close_writer(self):
        self.workbook.close()
