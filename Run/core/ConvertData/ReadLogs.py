# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import sqlalchemy
import functools
from random import uniform
from time import sleep
import re
from multiprocessing import Pool
import joblib
# analysis

import pandas as pd
import numpy as np
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import SMALLINT

# customize file
from Run.core.ConvertData.ConnectDB import sql_engine
from Run.core.ConvertData.ImportConf import bit_config, byte_config, drop_config
from Run.core.ConvertData.Config import WisselData
from Run.core.ConvertData.VerSelect import get_version, get_wissel_type_nr
from Run.core.ConvertData.ConnectDB import conn_engine
from Run.core.Integration.DataInitialization import get_alldata_from_db, save_to_sql


def read_log(log_file):
    """Read log data from wissel log file"""
    log_file_name = os.path.basename(log_file)
    date = f'{log_file_name[:4]}-{log_file_name[4:6]}-{log_file_name[6:8]}'
    wissel_data_dict = {}
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as (log):
        exclude_list = ['##', 'W657', 'W666', 'W662', 'W665', 'W668', 'W540', '_LSA_', 'W260']
        # exclude_list = ['##', 'W666', 'W662','W665', 'W668', '_LSA_']
        include_dict = {'WESTVEST_LSA': 'LSA_689', 'HS_W656_LSA': 'LSA_655',
                        'TTPW_LSA': 'LSA_018'}  #'TTHS_LSA': 'LSA_130',}
        for line in log:
            if 'DATA:PZDA' in line:
                if any(i in line for i in include_dict.keys()):
                    wissel_nr = include_dict.get([i for i in include_dict.keys() if i in line][0])
                    if wissel_nr in wissel_data_dict:
                        wissel_data_dict[wissel_nr].append(line[: -1])
                    else:
                        wissel_data_dict[wissel_nr] = [line[: -1]]
                elif any(i in line for i in exclude_list):
                    pass
                elif 'DATA:PZDA' in line and re.search(r'W\d\d\d', line) is not None:
                    wissel_nr = [re.search(r'W\d\d\d', line).group()]
                    wissel_nr = wissel_nr[0]
                    if wissel_nr in wissel_data_dict:
                        wissel_data_dict[wissel_nr].append(line[: -1])
                    else:
                        wissel_data_dict[wissel_nr] = [line[: -1]]
            else:
                pass
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
        else:
            dtypedict.update({i: SMALLINT()})
    return dtypedict


def conver_log_data(log_data, db_name, keys):
    bit_configs = bit_config()
    byte_configs = byte_config()
    conver_data_value = functools.partial(conver_data, bit_configs, byte_configs)
    data = list(map(conver_data_value, log_data.get(keys)))
    df_data_list = list(map(dataframe_str, data))
    df_data = pd.concat(df_data_list, ignore_index=True)
    # 去除重复项
    df_data = df_data.drop_duplicates()
    dtypedict = mapping_df_types(df_data)
    df_data.set_index('date-time', drop=True, inplace=True)
    df_data.sort_values(by='date-time')
    try:
        sleep(uniform(0.01, 0.2))
        engine = sql_engine(db_name)
        sqlite_connection = engine.connect()
        df_data.to_sql(keys, sqlite_connection, if_exists='replace', dtype=dtypedict)
    except:
        pass


def log_to_sql(log_data, db_name):
    """Convert log file to database"""
    try:
        wissel_nr_list = list(log_data.keys())
        convert_data_to_sql = functools.partial(conver_log_data, log_data, db_name)
        with Pool(16) as p:
            p.map(convert_data_to_sql, wissel_nr_list)

    except KeyboardInterrupt:
        exit()
    return None


def dataframe_str(value):
    df_single_data = pd.DataFrame(value, dtype='str')
    return df_single_data


def sub_set_steps(db_file, steps, k):
    wissel_status = pd.merge(pd.read_sql_table(k, conn_engine(db_file)), steps, how='left')
    wissel_status.set_index('date-time', drop=True, inplace=True)
    try:
        sleep(uniform(0.01, 0.2))
        wissel_status.to_sql(k, conn_engine(db_file), if_exists='replace')
    except:
        pass


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
        set_steps = functools.partial(sub_set_steps, db_file,steps)
        with Pool(16) as p:
            p.map(set_steps, table_name)

        # for k in table_name:
        #     wissel_status = pd.merge(pd.read_sql_table(k, conn_engine(db_file)), steps, how='left')
        #     wissel_status.set_index('date-time', drop=True, inplace=True)
        #     wissel_status.to_sql(k, conn_engine(db_file), if_exists='replace')
    except KeyboardInterrupt:
        exit()


def predict_steps(db_file):

    # 有效数据列表
    ini_list = ["<wissel> naar links", "<wissel> naar rechts", "<wissel> links", "<wissel> rechts",
                "<vlsa> links", "<vlsa> rechts", "<wls> seinbeld links geactiveerd",
                "<wls> seinbeld rechts geactiveerd", "<hfp> spoorstroomkring bezet", "<hfk> aanwezigheidslus bezet",
                "<vecom> naar links", "<vecom> naar midden", "<vecom> naar rechts",
                "<vecom> lock","<vecom> uit melding", "<wissel> vergrendeld", "<wissel> ijzer", "<loop 1> bezet",
                "<loop 2> bezet", "<loop 3> bezet", "<loop 4> bezet","<loop 5> bezet", "<loop 6> bezet",
                "<loop 7> bezet", "<loop 8> bezet", "<input> naar links", "<input> naar rechts", "<input> naar midden"]
    # 加载model
    model_list = [i[:-4] for i in os.listdir(os.path.join(rootPath, 'Run', 'conf', 'pipfiles')) if '.pkl' in i]
    model_dict = {i: joblib.load(os.path.join(rootPath, 'Run', 'conf', 'pipfiles', f'{i}.pkl')) for i in model_list}

    # 读取工作数据
    test_data_dict = get_alldata_from_db(db_file, 'db')
    for key, value in model_dict.items():
        try:
            test_data = test_data_dict.get(key)
            wissel_data_ini = test_data[ini_list]
            # 数据转换为numpy
            X = np.array(wissel_data_ini)
            # 模型预测
            y = value.predict(X)
            # test_data['predict step'] = y
            # 代替set_steps_denbdb3c
            test_data['predict step'] = y
            test_data_dict[key] = test_data
        except (TypeError, ValueError) as err:
            pass
    save_to_sql(db_file, test_data_dict, path='db')

