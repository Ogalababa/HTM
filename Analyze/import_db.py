# ！/usr/bin/python3
# coding:utf-8
from tqdm import tqdm

from __init__ import *
import pandas as pd
import sqlalchemy
from DataBase.ConnectDB import conn_engine


def get_all_wissel_data(log_db):

    """
    :param log_db: str
    :return dict
    """

    insp = sqlalchemy.inspect(conn_engine(log_db))
    all_wissel_name = insp.get_table_names()
    data_dict = {}
    for wissel_nr in tqdm(all_wissel_name):
        try:
            wissel_data = pd.read_sql_table(wissel_nr, conn_engine(log_db))
            wissel_data['date-time'] = pd.to_datetime(wissel_data['date-time'])
            data_dict[wissel_nr] = wissel_data

        except (ValueError, TypeError, KeyError) as err:
            print(err)
            pass

    return data_dict
