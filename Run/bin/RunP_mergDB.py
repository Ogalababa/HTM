# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import pandas as pd

from Run.core.Integration.DataInitialization import get_alldata_from_db
from Run.core.Integration.DataInitialization import save_to_sql


def concat_db(db_dir_list: list, path: str, file_name: str):
    """

    :param file_name: str file_name to save
    :param path: str
    :param db_dir_list: list
    :return: None
    """

    data_dict = {}
    for i in db_dir_list:
        if len(data_dict) == 0:
            data_dict = get_alldata_from_db(i, path)
        else:
            single_data_dict = get_alldata_from_db(i, path)
            for key, value in single_data_dict.items():
                if key in data_dict.keys():
                    data_dict[key] = pd.concat([data_dict.get(key), value], ignore_index=True).drop_duplicates()
                else:
                    data_dict[key] = value

    save_to_sql(file_name, data_dict, path)
