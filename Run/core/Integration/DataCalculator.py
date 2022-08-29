# ！/usr/bin/python3
# coding:utf-8
# sys
import os.path

from __init__ import *
import pandas as pd
from multiprocessing import Pool, Manager
from Run.core.Analyze.check_storing_df import check_storing_df, define_storing, define_storing_int
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
        self.error_list = Manager().list()
        self.wissel_nr_list = list(self.db_dict.keys())
        # self.speed_dict = {}

    def sub_tram_speed_(self, wissel_nr):
        speed_dict = {}
        try:
            values = self.db_dict.get(wissel_nr)
            # set to time format
            values['date-time'] = pd.to_datetime(values['date-time'])
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
                speed_dict[wissel_nr] = speed_df_list[0]
            else:
                speed_dict[wissel_nr] = pd.concat(speed_df_list)
            save_to_sql(self.db_name, speed_dict, 'snelheid')
        except:
            pass

    def C_tram_speed(self):
        """
        Calculate tram speed while tram passing the wissel
        :return: dict
        """
        # wiessl_nr_list = list(self.db_dict.keys())
        with Pool(16) as p:
            p.map(self.sub_tram_speed_, self.wissel_nr_list)

    def sub_wissel_schakel_(self, wissel_nr):
        data_dict = {}
        try:
            values = self.db_dict.get(wissel_nr)
            status_list = []
            index_list = wissel_cycle_list(values)
            for i in range(len(index_list) - 1):
                cycle_df = values[index_list[i]:index_list[i + 1]]
                if check_storing_df(cycle_df):
                    self.error_list.append(cycle_df)
                else:
                    schakel_status = wissel_schakel(cycle_df)
                    status_list.append(schakel_status[0])
                    # self.error_list.append(cycle_df)
                    if len(schakel_status) > 1:
                        self.error_list.append(schakel_status[1])
            data_dict[wissel_nr] = pd.concat(status_list)
            save_to_sql(self.db_name, data_dict, 'schakelen')
        except:
            pass

    def C_wissel_schakel(self):
        """
        Calculate wissel switch from database
        :return: save to sqlite3 file
        """
        with Pool(16) as p:
            p.map(self.sub_wissel_schakel_, self.wissel_nr_list)

    def C_storingen(self):
        storing_list = []
        storingen_dict = {}
        unknow_storing_list = []
        unknow_storing_dict = {}
        all_storing_dict = {}

        for i in self.error_list:
            try:
                unknow_state, storing = define_storing_int(i)
                if unknow_state == 'ontbekend':
                    unknow_storing_list.append(i)
                elif unknow_state == 'not_error':
                    pass
                elif unknow_state == 'invalid data':
                    pass
                else:
                    storing_list.append(storing)
            except:
                pass
        if len(storing_list) > 0:
            storingen_dict['all storingen'] = pd.concat(storing_list)
            # x = 0
            # for i in storing_list:
            #     storingen_dict[str(x).zfill(4)] = i
            #     x += 1
            if f'{self.db_name}.db' in os.listdir(os.path.join(rootPath, 'DataBase', 'storing')):
                os.remove(os.path.join(rootPath, 'DataBase', 'storing', f'{self.db_name}.db'))
            save_to_sql(self.db_name, storingen_dict, 'storing')
        if len(unknow_storing_list) > 0:
            x = 0
            for i in unknow_storing_list:
                unknow_storing_dict[str(x).zfill(3)] = i
                x += 1
            if f'{self.db_name}.db' in os.listdir(os.path.join(rootPath, 'DataBase', 'unknow_storing')):
                os.remove(os.path.join(rootPath, 'DataBase', 'unknow_storing', f'{self.db_name}.db'))
            save_to_sql(self.db_name, unknow_storing_dict, 'unknow_storing')

    def get_wissel_cycles(self, df):
        cycle_index = wissel_cycle_list(df)
        cycle_list = []
        for i in range(len(cycle_index) - 1):
            cycle_list.append(df[cycle_index[i]:cycle_index[i + 1]])
        return cycle_list
    
    def C_storingen_2(self):
        storing_list = []
        storingen_dict = {}
        unknow_storing_list = []
        unknow_storing_dict = {}
        for key, values in self.db_dict.items():
            if 'step' in values.columns.values.tolist():
                cycle_list = self.get_wissel_cycles(values)
                for i in cycle_list:
                    if check_storing_df(i):
                        unknow_state, storing = define_storing_int(i)
                        if unknow_state == 'ontbekend':
                            unknow_storing_list.append(i)
                        elif unknow_state == 'not_error':
                            pass
                        elif unknow_state == 'invalid data':
                            pass
                        else:
                            storing_list.append(storing)
        if len(storing_list) > 0:
            storingen_dict['all storingen'] = pd.concat(storing_list)
            # x = 0
            # for i in storing_list:
            #     storingen_dict[str(x).zfill(4)] = i
            #     x += 1
            if f'{self.db_name}.db' in os.listdir(os.path.join(rootPath, 'DataBase', 'storing')):
                os.remove(os.path.join(rootPath, 'DataBase', 'storing', f'{self.db_name}.db'))
            save_to_sql(self.db_name, storingen_dict, 'storing')
        if len(unknow_storing_list) > 0:
            x = 0
            for i in unknow_storing_list:
                unknow_storing_dict[str(x).zfill(3)] = i
                x += 1
            if f'{self.db_name}.db' in os.listdir(os.path.join(rootPath, 'DataBase', 'unknow_storing')):
                os.remove(os.path.join(rootPath, 'DataBase', 'unknow_storing', f'{self.db_name}.db'))
            save_to_sql(self.db_name, unknow_storing_dict, 'unknow_storing')

