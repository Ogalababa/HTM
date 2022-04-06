# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *


def check_storing_df(df):
    """
    Check dataframe is correct data, if not return False
    :param df: DataFrame
    :return: boolean
    """
    check_error_list = [
        len(set(df["<vecom> track zonder vergrendeling"])) > 1,
        len(set(df["<wissel> ijzer"])) > 1,
        len(set(df["<vecom> com. fout ifc"])) > 1,
        len(set(df["<vecom> lus zonder richting"])) > 1,
        len(set(df["<aanmelden> wagen"])) > 2,
    ]
    if any(check_error_list):
        return True
    else:
        return False
