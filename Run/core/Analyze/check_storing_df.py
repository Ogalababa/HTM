#!/usr/bin/ python3
# coding: utf-8
from __init__ import *


from Run.core.Analyze.analyze_tool import *
import pandas as pd
from collections import OrderedDict


def check_storing_df(dataset):
    """
    Check dataframe is correct data, if not return False
    :param df: DataFrame
    :return: boolean
    """
    # filter data from reniging
    df = dataset[(dataset['<wissel> op slot'] != 0) | (dataset['<wissel> ijzer'] != 0)]
    check_error_list = [
        len(set(df["<vecom> track zonder vergrendeling"])) > 1,
        len(set(df["<wissel> ijzer"])) > 1,
        len(set(df["<vecom> com. fout ifc"])) > 1,
        len(set(df["<vecom> lus zonder richting"])) > 1,
        len(set(df["<aanmelden> wagen"])) > 2,
        len(set(df["<wissel> op slot"])) < 2
    ]
    return any(check_error_list)


def recheck_storing(dataset):
    try:
        # cleaning dataset
        df = dataset[(dataset['<wissel> op slot'] != 0) | (dataset['<wissel> ijzer'] != 0)]
        step_revert = 0
        step_list = df['step']
        step_list = [i for i in step_list if i is not None]
        # is_storing = False
        for i in range(len(step_list)-1):
            if step_list[i+1] < step_list[i]:
                step_revert += 1

        return any([step_revert > 3 + (max(df['<aktuell> niveau fifo']) + len(set(df['<aktuell> wagen']))) * 2,
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
        'Wissel Nr': [dataset.iloc[1]['wissel nr']],
        'lijn nr': [dataset.iloc[2]['<aanmelden> lijn']],
        'service': [dataset.iloc[2]['<aanmelden> service']],
        'categorie': [dataset.iloc[2]['<aanmelden> categorie']],
        # 'wagen nr': [ i for i in list(set(dataset['<aktuell> wagen'].tolist())) if i != 0]
    }
    storing = ['ontbekend']
    afdelling = ['ontbekend']

    func_dict = OrderedDict([
        (wissel_buiten_dinst(dataset), [['wissel buiten dienst'], ['infra']]),
        (wissel_eind_stand(dataset), [['wissel heeft geen eind stand'], ['infra']]),
        (check_bad_contact(dataset, '<hfp> schakelcriterium bezet'), [['HFP slecht contact'], ['infra']]),
        (check_bad_contact(dataset, '<hfk> schakelcriterium bezet'), [['HFK slecht contact'], ['infra']]),
        (check_fout_state(dataset, '<vecom> track zonder vergrendeling'), [['wissel kan lijn nr niet handelen'], ['wagen']]),
        (check_fout_state(dataset, '<vecom> com. fout ifc'), [['VECOM error'], ['infra']]),
        (check_fout_state(dataset, '<vecom> lus zonder richting'), [['lijn nr niet in de handel lijst'], ['wagen']]),
        (check_werk_wagen(dataset), [['wissel kan werk de wagen niet afmeden'], ['werk wagen']]),
        (check_wagen_vecom(dataset), [['vecom in wagen slect contitie'], ['wagen']]),
        # (miss_out_meld(dataset), [['miss out meld lus'], ['vecom']]),
        (check_verkeerd_code(dataset), [['verkeerde code'], ['bestuurder']])
    ])
    for i in func_dict.keys():
        if i:
            storing, afdelling = func_dict.get(i)
            break
    storing_type['storing'] = storing
    storing_type['afdelling'] = afdelling
    storing_type['count'] = [1]
    return storing[0], pd.DataFrame(storing_type)

