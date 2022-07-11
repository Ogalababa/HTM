# ！/usr/bin/python3
# coding:utf-8
# sys
import os

from __init__ import *
from Run.core.Integration.DataInitialization import get_alldata_from_db, save_to_sql
import pandas as pd


def mix_storing():

    db_list = [i[:-3] for i in os.listdir(os.path.join(rootPath, 'DataBase', 'storing')) if '.db' in i]
    total_df_list = []
    db_list.sort()
    for i in db_list:
        try:
            date_storing = get_alldata_from_db(i, path='storing').get('all storingen')
            # data_storing = date_storing[date_storing['wissel stop'] == 1]
            date_storing = date_storing[date_storing['begin tijd'].str.contains('00-|-00') == False]
            date_storing['datum'] = pd.to_datetime(date_storing['begin tijd']).dt.date
            total_df_list.append(date_storing)
            # total_df_list.append(date_storing[date_storing['wissel stop'] == 1])
        except:
            print(i)
    mixed_dict = {'all data': pd.concat(total_df_list)}
    print(total_df_list[0].head())
    save_to_sql('storing', mixed_dict, path='rapport')


if __name__ == '__main__':
    mix_storing()
