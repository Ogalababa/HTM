# ！/usr/bin/python3
# coding:utf-8
# sys
import pandas as pd

from Run.core.Analyze.check_storing_df import check_storing_df, define_storing
from Run.core.Analyze.tram_speed import calculation_tram_speed
from Run.core.Analyze.wissel_schakel import wissel_schakel
from Run.core.Analyze.wissel_vrij_list import wissel_cycle_list
from Run.core.Integration.DataInitialization import get_alldata_from_db
from Run.core.Integration.DataInitialization import save_to_sql


class Calculator:
    """
    Get data from log database
    Calculate log data to useful data
    """

    def __init__(self, db_name):
        """
        Initialization data from sqlite3 db to dict with key = table name
        :param db_name: dict
        """
        self.db_name = db_name
        self.db_dict = get_alldata_from_db(db_name, path='db')
        self.error_list = []

    def C_tram_speed(self):
        """
        Calculate tram speed while tram passing the wissel
        :return: dict
        """
        speed_dict = {}
        for key, values in self.db_dict.items():

            # set to time format
            values['date-time'] = pd.to_datetime(values['date-time'])
            # check cycles
            try:
                index_list = wissel_cycle_list(values)
                speed_df_list = []
                for i in range(len(index_list) - 1):
                    cycle_df = values[index_list[i]:index_list[i + 1]]
                    speed_df = calculation_tram_speed(cycle_df)
                    if len(speed_df) == 0:
                        pass
                    elif len(speed_df) == 1:
                        speed_df_list.append(speed_df[0])
                    else:
                        speed_df_list.append(pd.concat(speed_df))
                if len(speed_df_list) == 0:
                    pass
                elif len(speed_df_list) == 1:
                    speed_dict[key] = speed_df_list[0]
                else:
                    speed_dict[key] = pd.concat(speed_df_list)
            except:
                pass

        save_to_sql(self.db_name, speed_dict, 'snelheid')

    def C_wissel_schakel(self):
        """
        Calculate wissel switch from database
        :return: save to sqlite3 file
        """
        data_dict = {}

        for key, values in self.db_dict.items():
            try:
                status_list = []
                index_list = wissel_cycle_list(values)
                for i in range(len(index_list) - 1):
                    cycle_df = values[index_list[i]:index_list[i + 1]]
                    if check_storing_df(cycle_df):
                        self.error_list.append(cycle_df)
                    else:
                        schakel_status = wissel_schakel(cycle_df)
                        status_list.append(schakel_status[0])
                        if len(schakel_status) > 1:
                            self.error_list.append(schakel_status[1])
                data_dict[key] = pd.concat(status_list)

            except(KeyError, IndexError, ValueError, TypeError, ZeroDivisionError):
                pass

        save_to_sql(self.db_name, data_dict, 'schakelen')

    def C_storingen(self):
        storing_list = []
        storingen_dict = {}
        unknow_storing_list = []
        unknow_storing_dict = {}
        all_storing_dict = {}
        # self.error_list = [i for i in self.error_list if '<wissel> op slot' in i.tolist()]
        # self.error_list = [i for i in self.error_list if len(set(i['<wissel> op slot'])) > 0]
        # self.error_list = [i for i in self.error_list if recheck_storing(i) is True]
        for i in self.error_list:
            try:
                unknow_state, storing = define_storing(i)
                if unknow_state == 'ontbekend':
                    unknow_storing_list.append(i)
                elif unknow_state == 'noerror':
                    pass
                elif unknow_state == 'invalid data':
                    pass
                else:
                    storing_list.append(storing)
            except:
                pass
        if len(storing_list) > 0:
            storingen_dict['all storingen'] = pd.concat(storing_list)
            save_to_sql(self.db_name, storingen_dict, 'storing')
        if len(unknow_storing_list) > 0:
            x = 0
            for i in unknow_storing_list:
                unknow_storing_dict[str(x).zfill(3)] = i
                x += 1
            save_to_sql(self.db_name, unknow_storing_dict, 'unknow_storing')
        if len(self.error_list) > 0:
            x = 0
            for i in self.error_list:
                all_storing_dict[str(x).zfill(3)] = i
                x += 1
            save_to_sql(self.db_name, all_storing_dict, 'all_storing')
