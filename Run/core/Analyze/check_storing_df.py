#!/usr/bin/ python3
# coding: utf-8
from Run.core.Analyze.analyze_tool import match_list, check_bad_contact, check_fout_state
from __init__ import *

import pandas as pd



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
    """
    define storing type.
    :param dataset: pd.DataFrame
    :return: str, pd.DataFrame
    """
    storing_type = {
        'begin tijd': [dataset.iloc[1]['date-time']],
        'eind tijd': [dataset.iloc[-1]['date-time']],
        'wissel nr': [dataset.iloc[1]['wissel nr']],
        'lijn nr': [dataset.iloc[2]['<aanmelden> lijn']],
        'service': [dataset.iloc[2]['<aanmelden> service']],
        'categorie': [dataset.iloc[2]['<aanmelden> categorie']]
                    }
    storing = ['ontbekend']
    afdelling = ['ontbekend']
    if check_bad_contact(dataset, '<hfp> schakelcriterium bezet'):
        storing = ['HFP slecht contact']
        afdelling = ['infra']
    if check_bad_contact(dataset, '<hfk> schakelcriterium bezet'):
        storing = ['HFK slecht contact']
        afdelling = ['infra']
    if check_fout_state(dataset, '<vecom> track zonder vergrendeling'):
        storing = [f'wissel kan lijn nr {storing_type.get("lijn nr")} niet handelen']
        afdelling = ['wagen']
    if check_fout_state(dataset, '<vecom> com. fout ifc'):
        storing = ['VECOM error']
        afdelling = ['infra']
    if check_fout_state(dataset, '<vecom> lus zonder richting'):
        storing = [f'lijn nr {storing_type.get("lijn nr")} niet in de handel lijst']
        afdelling = ['wagen']
    storing_type['storing'] = storing
    storing_type['afdelling'] = afdelling

    return storing[0], pd.DataFrame(storing_type)

