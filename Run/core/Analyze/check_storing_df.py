#!/usr/bin/ python3
# coding: utf-8
from __init__ import *

from Run.core.Analyze.analyze_tool import *
import pandas as pd


# Check if the data is normal
# 检测数据是否正常
def check_storing_df(dataset):
    """
    Check dataframe is correct data, if not return False
    :param dataset: DataFrame
    :return: boolean
    """
    # filter data from reniging
    df = dataset[(dataset['<wissel> vergrendeld'] != 0) | (dataset['<wissel> ijzer'] != 0)]
    check_error_list = [
        len(set(df["<vecom> aanvraag onbekend"])) > 1,
        len(set(df["<wissel> ijzer"])) > 1,
        len(set(df["<vecom> storing"])) > 1,
        len(set(df["<vecom> geen output"])) > 1,
        len(set(df["<aanmelden> wagen"])) > 2,  # !!!!
        len(set(df["<wissel> vergrendeld"])) < 2
    ]
    return any(check_error_list)


# Check again if the data is normal
# 再次检测数据是否正常
def recheck_storing(dataset):
    try:
        # cleaning dataset
        df = dataset[(dataset['<wissel> vergrendeld'] != 0) | (dataset['<wissel> ijzer'] != 0)]
        step_revert = 0
        step_list = df['step']
        step_list = [i for i in step_list if i is not None]
        # is_storing = False
        for i in range(len(step_list) - 1):
            if step_list[i + 1] < step_list[i]:
                step_revert += 1

        return any([step_revert > 3 + (max(df['<aktuell> niveau fifo']) + len(set(df['<aktuell> wagen']))) * 2,
                    0 in df['<wissel> ijzer'].to_list(),
                    match_list([1, 0, 1], df['<hfp> spoorstroomkring bezet'].to_list()),
                    match_list([1, 0, 0, 1], df['<hfp> spoorstroomkring bezet'].to_list()),
                    match_list([1, 0, 0, 1], df['<hfk> aanwezigheidslus bezet'].to_list()),
                    match_list([1, 0, 1], df['<hfk> aanwezigheidslus bezet'].to_list())])
    except:
        return True

    
# Parse error data
# 分析错误数据
def define_storing(dataset):
    """
    define storing type.
    :param dataset: pd.DataFrame
    :return: str, pd.DataFrame
    """

    error_info = None
    wagen_nr = max(dataset['<aanmelden> wagen'].tolist(), key=dataset['<aanmelden> wagen'].tolist().count)
    storing_type = {
        'begin tijd': [dataset.iloc[1]['date-time']],
        'eind tijd': [dataset.iloc[-1]['date-time']],
        'Wissel Nr': [dataset.iloc[1]['wissel nr']],
        'lijn nr': [dataset[dataset['<aanmelden> wagen'] == wagen_nr].iloc[0]['<aanmelden> lijn']],
        'service': [dataset[dataset['<aanmelden> wagen'] == wagen_nr].iloc[0]['<aanmelden> service']],
        'categorie': [dataset[dataset['<aanmelden> wagen'] == wagen_nr].iloc[0]['<aanmelden> categorie']],
        'wagen nr': [wagen_nr],
        'wissel stop': [(min(dataset['<wissel> ijzer']) - 1) * -1]
    }
    storing = ['ontbekend']
    afdelling = ['ontbekend']
    func_list = [
        # Sorting method: Arrange from top to bottom according to the detection index
        # 排序方式：根据检测index从上到下排列
        # 0
        small_dataset(dataset, 'invalid data', 'system'),
        # 1
        hfk_defect(dataset, 'HFK defect', 'infra'),
        # 2
        wissel_buiten_dinst(dataset, 'wissel buiten dienst', 'infra'),
        # 3
        double_wissels(dataset, 'not_error', 'double wissels'),
        # 4
        no_wagen_nr(dataset, 'wagen zonder vecom', 'wagen'),
        # 5
        wissel_eind_stand(dataset, 'wissel heeft geen eind stand', 'infra'),
        # 6
        check_fout_state(dataset, '<vecom> aanvraag onbekend', 'categorie/handbedien code fout', 'bestuurder'),
        # 7
        check_bad_contact(dataset, '<hfp> spoorstroomkring bezet', 'HFP detector fout', 'infra'),
        # 8
        check_bad_contact(dataset, '<hfk> aanwezigheidslus bezet', 'HFK detector fout', 'infra'),
        # 9
        hfk_defect(dataset, 'HFK defect', 'infra'),
        # 10
        check_wagen_vecom(dataset, 'vecom in wagen fout', 'wagen'),
        # 11
        miss_out_meld(dataset, 'afmelden fout', 'infra'),
        # 12
        wacht_op_sein(dataset, 'bestuurder wacht niet op sein', 'bestuurder'),
        # 13
        check_fout_state(dataset, '<vecom> storing', 'VECOM hardware fout', 'infra'),
        # 14
        check_fout_state(dataset, '<vecom> geen output', 'Elektronisch blokkeren', 'bestuurder'),
        # 15
        check_werk_wagen(dataset, 'wissel kan de werk wagen niet afmeden', 'infra'),
        # 16
        check_verkeerd_code(dataset, 'richting-code richting niet overeen', 'bestuurder'),
        # 17
        double_input(dataset, 'richting veranderen na de aanvragen', 'bestuurder'),
        # 18
        no_aktuell(dataset, 'bestuurder rit te vroeg naar de hfp', 'bestuurder'),
    ]
    try:
        storing_type['wagen nr'] = [i for i in dataset['<aktuell> wagen'].tolist() if i != 0][0]
    except:
        storing_type['wagen nr'] = [0]
    for error_info in func_list:
        if error_info[-1]:
            #  error_info = i
            storing = [error_info[0]]
            afdelling = [error_info[1]]
            if len(error_info) == 7:
                storing_type['lijn nr'] = [error_info[2]]
                storing_type['service'] = [error_info[3]]
                storing_type['categorie'] = [error_info[4]]
                storing_type['wagen nr'] = [error_info[5]]
            break
        elif recheck_storing(dataset) is not True:
            storing = ['not_error']
    storing_type['storing'] = storing
    storing_type['afdelling'] = afdelling
    storing_type['count'] = [1]

    return storing[0], pd.DataFrame(storing_type)