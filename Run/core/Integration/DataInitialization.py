# ！/usr/bin/python3
# coding:utf-8
# sys
import os

from __init__ import *
import sqlalchemy
import pandas as pd
from Run.core.ConvertData.ConnectDB import conn_engine


def get_database_list(path='db'):
    """Get database name from dir
    :return: list
    """
    all_db_file = os.listdir(os.path.join(dataPath, path))

    return [i[:-3] for i in all_db_file if i[-3:] == '.db']


def get_alldata_from_db(db_name, path='db'):
    """Get data info from db file
    :return: dict
    """
    data_dict = {}
    insp = sqlalchemy.inspect(conn_engine(db_name, path))
    tables = insp.get_table_names()
    for name in tables:
        data_dict[name] = pd.read_sql_table(name, conn_engine(db_name, path))

    return data_dict


def save_to_sql(db_name, data_dict, path):
    """
    Save calculated data to sql
    :param db_name: database name
    :param data_dict: {wissel_nr:dataframe}
    :param path: database dir
    :return: None
    """
    if len(data_dict.keys()) < 2:
        table_name = list(data_dict.keys())[0]
        value = data_dict.get(table_name)
        value.to_sql(table_name, conn_engine(db_name, path), index=False, if_exists='replace')
    else:
        for key, value in data_dict.items():
            try:
                value.to_sql(key, conn_engine(db_name, path), index=False, if_exists='replace')

            except:
                pass
    return None
