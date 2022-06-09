# ！/usr/bin/python3
# coding:utf-8
# sys
import pandas as pd


def wissel_cycle_list(df):
    """
    Calculate wissel status cycles, return index nr when wissel is free
    :param df: wissel status dataframe
    :return: list with dataframe index nr
    """
    index_list = df[df['<wissel> vergrendeld'] == 0].index.values.tolist()
    if 0 not in index_list:
        index_list.insert(0,0)
    index_nr = 0
    drop_list = []
    for i in range(1, len(index_list) - 1):
        if index_list[i] - index_nr < 5:
            index_nr = index_list[i]
            drop_list.append(index_list[i])
        else:
            index_nr = index_list[i]
    return [i for i in index_list if i not in drop_list]
