# ！/usr/bin/python3
# coding:utf-8
from __init__ import *

import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm


def root_path():
    current_path = os.path.dirname(os.path.realpath(__file__))
    current_dir = os.path.basename(current_path)
    main_path = f'{current_path.replace(current_dir, "")}'
    return main_path


def sql_engine(db_name, path='db'):
    db_path = os.path.join(root_path(), 'DataBase', path, f'{db_name}.db')
    return create_engine(f'sqlite:///{db_path}', )


def conn_engine(db_name, path='db'):
    engine = sql_engine(db_name, path)
    return engine.connect()


def intialization_sql(sql_table, columns, sqlite_connection):
    sql_columns_list = []
    set_sql_table = {}
    for column in tqdm(columns, desc='collect sql columns'):
        sql_columns_list.extend(column)
        sql_columns_list = list(set(sql_columns_list))
    for column in tqdm(sql_columns_list, desc='Prepare sql columns'):
        set_sql_table[column] = []

    df = pd.DataFrame(set_sql_table, dtype='str')
    df.set_index('date-time', drop=True, inplace=True)
    # Write database
    df.to_sql(sql_table, sqlite_connection, if_exists='replace')


def connect_sql3(database):
    engine = create_engine(f'sqlite:///db//{database}.db')
    sqlite_connection = engine.connect()
    return sqlite_connection
