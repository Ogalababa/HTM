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
    df = dataset[(dataset['<wissel> op slot'] != 0) | (dataset['<wissel> ijzer'] != 0)]
    check_error_list = [
        len(set(df["<vecom> track zonder vergrendeling"])) > 1,
        len(set(df["<wissel> ijzer"])) > 1,
        len(set(df["<vecom> com. fout ifc"])) > 1,
        len(set(df["<vecom> lus zonder richting"])) > 1,
        len(set(df["<aanmelden> wagen"])) > 2,  # !!!!
        len(set(df["<wissel> op slot"])) < 2
    ]
    return any(check_error_list)


# Check again if the data is normal
# 再次检测数据是否正常
def recheck_storing(dataset):
    try:
        # cleaning dataset
        df = dataset[(dataset['<wissel> op slot'] != 0) | (dataset['<wissel> ijzer'] != 0)]
        step_revert = 0
        step_list = df['step']
        step_list = [i for i in step_list if i is not None]
        # is_storing = False
        for i in range(len(step_list) - 1):
            if step_list[i + 1] < step_list[i]:
                step_revert += 1

        return any([step_revert > 3 + (max(df['<aktuell> niveau fifo']) + len(set(df['<aktuell> wagen']))) * 2,
                    0 in df['<wissel> ijzer'].to_list()])
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
        wissel_buiten_dinst(dataset, 'wissel buiten dienst', 'infra'),
        # 2
        no_wagen_nr(dataset, 'wagen zonder vecom', 'wagen'),
        # 3
        wissel_eind_stand(dataset, 'wissel heeft geen eind stand', 'infra'),
        # 4
        check_fout_state(dataset, '<vecom> track zonder vergrendeling', 'categorie/handbedien code fout', 'bestuurder'),
        # 5
        check_bad_contact(dataset, '<hfp> schakelcriterium bezet', 'HFP detector fout', 'infra'),
        # 6
        check_bad_contact(dataset, '<hfk> schakelcriterium bezet', 'HFK detector fout', 'infra'),
        # 7
        check_wagen_vecom(dataset, 'vecom in wagen fout', 'wagen'),
        # 8
        miss_out_meld(dataset, 'afmelden fout', 'infra'),
        # 9
        wacht_op_sein(dataset, 'bestuurder wacht niet op sein', 'bestuurder'),
        # 10
        check_fout_state(dataset, '<vecom> com. fout ifc', 'VECOM hardware fout', 'infra'),
        # 11
        check_fout_state(dataset, '<vecom> lus zonder richting', 'categorie/handbedien code fout', 'bestuurder'),
        # 12
        check_werk_wagen(dataset, 'wissel kan werk de wagen niet afmeden', 'werk wagen'),
        # 13
        check_verkeerd_code(dataset, 'richting-code richting niet overeen', 'bestuurder'),
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