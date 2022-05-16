# ！/usr/bin/python3
# coding:utf-8
# sys

from Run.core.Analyze.analyze_tool import check_bad_contact
import pandas as pd
from Run.core.Tools.VaribleTool import wissel_gerade


def wagen_lent(wagen_nr):
    """
    default wagen lent
    :param wagen_nr: int
    :return: int
    """
    if 3000 <= wagen_nr < 4000:
        lent = 30
    elif 4000 <= wagen_nr < 5000:
        lent = 37
    elif 5000 <= wagen_nr < 6000:
        lent = 35
    else:
        lent = 0
    return lent


def calculation_tram_speed(dataset):
    """
    calculation the tram speed
    :param dataset: pd.DataFrame
    :return: pd.DataFrame
    """
    speed_df_list = []
    try:
        # 筛选wagen数据
        wagen_set = set(dataset[dataset['<hfk> schakelcriterium bezet'] == 1]['<afmelden> wagen'].tolist())
        # 筛选wagen通过wissel数据集
        for i in wagen_set:
            richting = 'ontbekend'
            hfk_df = dataset[dataset['<afmelden> wagen'] == i]
            # 判断数据正确性
            hfk_index_list = hfk_df[hfk_df['<hfk> schakelcriterium bezet'] == 1].index.tolist()
            # 验证数据连续性
            continuity = dataset.loc[hfk_index_list[0]]['Count'] - dataset.loc[hfk_index_list[0] - 1]['Count']
            hfk_state = any([check_bad_contact(hfk_df, '<hfk> schakelcriterium bezet', 'hfk', 'infra')[-1],
                             continuity > 3])
            if hfk_state is not True:

                if len(hfk_index_list) >= 3:
                    speed_dict = {}
                    wissel_nr = dataset.loc[hfk_index_list[0]]['wissel nr']
                    lijn_nr = dataset[dataset['<aanmelden> wagen'] == i].iloc[0]['<aanmelden> lijn']
                    service = dataset[dataset['<aanmelden> wagen'] == i].iloc[0]['<aanmelden> service']
                    categorie = dataset[dataset['<aanmelden> wagen'] == i].iloc[0]['<aanmelden> categorie']
                    wagen_nr = dataset.loc[hfk_index_list[0]]['<afmelden> wagen']
                    # 判断行进方向
                    if dataset.loc[hfk_index_list[0]]['<wissel> links'] == 1:
                        richting = '<wissel> links'
                    elif dataset.loc[hfk_index_list[0]]['<wissel> rechts'] == 1:
                        richting = '<wissel> rechts'
                    if richting == wissel_gerade(wissel_nr):
                        richting = 'Recht door'
                    else:
                        richting = f'{richting[8:]} af'
                    # 储存数据
                    hfk_in = dataset.loc[hfk_index_list[0]]['date-time']
                    hfk_out = dataset.loc[hfk_index_list[-1] + 1]['date-time']
                    speed = round(wagen_lent(wagen_nr) / (hfk_out - hfk_in).total_seconds() * 3.6)

                    if speed < 50:
                        speed_dict['<aanmelden> lijn'] = [lijn_nr]
                        speed_dict['<afmelden> wagen'] = [wagen_nr]
                        speed_dict['<aanmelden> categorie'] = [categorie]
                        speed_dict['<aanmelden> service'] = [service]
                        speed_dict['wissel nr'] = [wissel_nr]
                        speed_dict['Richting'] = [richting]
                        speed_dict['hfk_in'] = [hfk_in]
                        speed_dict['hfk_uit'] = [hfk_out]
                        speed_dict['snelheid km/h'] = [speed]
                        # 转换成data frame
                        speed_df_list.append(pd.DataFrame(speed_dict))
                    else:
                        pass
                else:
                    pass
            else:
                pass
    except:
        pass
    return speed_df_list
