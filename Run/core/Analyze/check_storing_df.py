#!/usr/bin/ python3
# coding: utf-8

from __init__ import *

import pandas as pd
from Run.core.Tools.VaribleTool import match_list


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
        len(set(df["<wissel> op slot"])) < 2
    ]
    return any(check_error_list)


def recheck_storing(df):
    try:
        # cleaning dataset
        # df = dataset[(dataset['<wissel> op slot'] != 0) & (dataset['<wissel> ijzer'] != 0)]
        step_revert = 0
        step_list = df['step']
        step_list = [i for i in step_list if i is not None]
        # is_storing = False
        for i in range(len(step_list)-1):
            if step_list[i+1] < step_list[i]:
                step_revert += 1

        return any([step_revert > 3,
                    0 in df['<wissel> ijzer'].to_list(),
                    match_list([1, 0, 1], df['<hfp> schakelcriterium bezet'].to_list()),
                    match_list([1, 0, 0, 1], df['<hfp> schakelcriterium bezet'].to_list()),
                    match_list([1, 0, 0, 1], df['<hfk> schakelcriterium bezet'].to_list()),
                    match_list([1, 0, 1], df['<hfk> schakelcriterium bezet'].to_list())])
    except:
        return True


def define_storing(dataset):
    storing_type = {
        'begin tijd': [dataset.iloc[1]['date-time']],
        'eind tijd': [dataset.iloc[-1]['date-time']],
        'wissel nr': [dataset.iloc[1]['wissel nr']],
                    }
    storing = ['ontbekend']
    afdelling = ['ontbekend']
    if any([match_list([1, 0, 1], dataset['<hfp> schakelcriterium bezet'].to_list()),
           match_list([1, 0, 0, 1], dataset['<hfp> schakelcriterium bezet'].to_list())]):
        storing = ['HFP slect contact']
        afdelling = ['infra']
    if any([match_list([1, 0, 1], dataset['<hfk> schakelcriterium bezet'].to_list()),
           match_list([1, 0, 0, 1], dataset['<hfk> schakelcriterium bezet'].to_list())]):
        storing = ['HFK slect contact']
        afdelling = ['infra']

    storing_type['storing'] = storing
    storing_type['afdelling'] = afdelling

    return storing[0], pd.DataFrame(storing_type)

