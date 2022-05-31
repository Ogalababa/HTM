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
    data_list = os.listdir(os.path.join(rootPath, 'DataBase', path, f'{db_name}.db'))
    data_dict = {}
    if f'{db_name}.db' in data_list:
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
    for key, value in data_dict.items():
        try:
            value.to_sql(key, conn_engine(db_name, path), index=False, if_exists='replace')

        except (ValueError, TypeError, KeyError):
            pass
    return None
