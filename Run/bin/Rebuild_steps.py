# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *

from Run.core.ConvertData.VerSelect import get_wissel_type_nr
from multiprocessing import Pool
import pandas as pd
from Run.core.Integration.DataInitialization import get_alldata_from_db, save_to_sql
from datetime import datetime


def rebuid_steps_single(db_name):
    all_data_dict = get_alldata_from_db(db_name)
    for key, value in all_data_dict.items():
        if 'step' in value.columns.to_list():
            # value['step'] = value['step'].astype('float64')
            value['step'] = value['step'].map(
                {'10': '100', '1': '10', '2': '20', '3': '30', '4': '40', '5': '50', '6': '60', '7': '70', '8': '80',
                 '9': '90', '11': '110', '2.1': '21', '2.2': '22', '2.3': '23'})
            # value['step'] = value['step'].astype('int32')
    save_to_sql(db_name, all_data_dict, path='db')


if __name__ == '__main__':
    start = datetime.now()
    db_list = [i[:-3] for i in os.listdir(os.path.join(rootPath, 'DataBase', 'db')) if '.db' in i]
    # db_list.remove('2022-06-02')
    db_list.sort()
    # with Pool(10) as p:
    #     p.map(rebuid_steps_single, db_list)
    for i in db_list:
        rebuid_steps_single(i)
    end = datetime.now()
    print(f'total time: {(end - start).seconds} seconds')
