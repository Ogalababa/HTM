# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
import sqlalchemy
import functools
import gc
import re
# analysis

import pandas as pd
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import SMALLINT

# customize file
from Run.core.ConvertData.ConnectDB import sql_engine
from Run.core.ConvertData.ImportConf import bit_config, byte_config, drop_config
from Run.core.ConvertData.Config import WisselData
from Run.core.ConvertData.VerSelect import get_version, get_wissel_type_nr
from Run.core.ConvertData.ConnectDB import conn_engine


def read_log(log_file):
    """Read log data from wissel log file"""
    log_file_name = os.path.basename(log_file)
    date = f'{log_file_name[:4]}-{log_file_name[4:6]}-{log_file_name[6:8]}'
    wissel_data_dict = {}
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as (log):
        exclude_list = ['##', 'W657', 'W666', 'W662', 'W665', 'W668', 'W540', '_LSA_', 'W260']
        # exclude_list = ['##', 'W666', 'W662','W665', 'W668', '_LSA_']
        for line in log:
            if any(i in line for i in exclude_list):
                pass
            elif 'DATA:PZDA' in line and re.search(r'W\d\d\d', line) is not None:
                # header_data = ConvertData(line)
                wissel_nr = [re.search(r'W\d\d\d', line).group()]
                wissel_nr = wissel_nr[0]
                if wissel_nr in wissel_data_dict:
                    wissel_data_dict[wissel_nr].append(line[: -1])

                else:
                    wissel_data_dict[wissel_nr] = [line[: -1]]
    return wissel_data_dict, date


def conver_data(bit, byte, value):
    """Convert wissel log data to wissel satus"""
    row_data = WisselData(value, bit, byte)
    row_data.line_to_hex()
    row_data.list_to_str()
    row_data.hex_to_bin()
    wissel_nr = row_data.wissel_info.get('wissel nr')
    row_data.wissel_version(get_version(wissel_nr))
    converted_info = row_data.covert_data()

    return converted_info


def mapping_df_types(df):
    dtypedict = {}
    for i in df.columns:
        if "date-time" in i:
            dtypedict.update({i: VARCHAR()})
        elif "server time" in i:
            dtypedict.update({i: VARCHAR()})
        elif "wissel nr" in i:
            dtypedict.update({i: VARCHAR()})
        # elif "time" in i:
        #     dtypedict.update({i: VARCHAR()})
        # elif "status" in i:
        #     dtypedict.update({i: VARCHAR()})
        else:
            dtypedict.update({i: SMALLINT()})
    return dtypedict


def log_to_sql(log_data, db_name):
    """Convert log file to database"""
    try:
        bit_configs = bit_config()
        byte_configs = byte_config()
        drop_configs = drop_config()
        engine = sql_engine(db_name)
        sqlite_connection = engine.connect()

        for key, values in log_data.items():
            # Multy processing
            drop_list = drop_configs.get(get_version(key))
            conver_data_value = functools.partial(conver_data, bit_configs, byte_configs)
            data = list(map(conver_data_value, values))
            df_data_list = list(map(dataframe_str, data))
            df_data = pd.concat(df_data_list, ignore_index=True)
            dtypedict = mapping_df_types(df_data)
            df_data.set_index('date-time', drop=True, inplace=True)
            df_data.to_sql(key, sqlite_connection, if_exists='replace', dtype=dtypedict)
        del conver_data_value, data, df_data_list, df_data
        gc.collect()
    except KeyboardInterrupt:
        exit()
    return None


def dataframe_str(value):
    df_single_data = pd.DataFrame(value, dtype='str')
    return df_single_data


def set_steps_denbdb3c(db_file):
    """Set cycle steps for wissel type denbdb3c"""
    try:
        # 匹配 denDBD3C steps
        table_name = sqlalchemy.inspect(conn_engine(db_file)).get_table_names()
        fit_wissel_type = [
            *get_wissel_type_nr('denAJB1C'), *get_wissel_type_nr('denBDB3C'), *get_wissel_type_nr('denBDC1C'),
            *get_wissel_type_nr('denBYA1C'), *get_wissel_type_nr('denBXB2C')
        ]
        table_name = [i for i in table_name if i in fit_wissel_type]
        table_name.sort()
        # get denDBD3C steps
        steps = pd.read_sql_table('denBDB3C', conn_engine('steps', path='norm'))
        for k in table_name:
            wissel_status = pd.merge(pd.read_sql_table(k, conn_engine(db_file)), steps, how='left')
            wissel_status.set_index('date-time', drop=True, inplace=True)
            # df_data = df_data.set_index(['<aanmelden> wagen', '<aanmelden> categorie', '<aanmelden> service'],
            # drop=False, inplace=False)
            wissel_status.to_sql(k, conn_engine(db_file), if_exists='replace')
        del wissel_status
        gc.collect()
    except KeyboardInterrupt:
        exit()

