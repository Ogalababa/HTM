# ！/usr/bin/python3
# coding:utf-8
# sys
import os

from __init__ import *
from Run.core.Integration.DataInitialization import get_alldata_from_db, save_to_sql
import pandas as pd


def mix_speed(r_spped: int, l_speed: int):
    db_list = [i[:-3] for i in os.listdir(os.path.join(rootPath, 'DataBase', 'snelheid')) if '.db' in i]
    total_df_list = []
    db_list.sort()
    for i in db_list:
        speed_dict = get_alldata_from_db(i, path='snelheid')
        to_frame_dict = {'datum': i}
        recht_door_over_load_count = 0
        af_over_load_count = 0
        total_recht_count = 0
        total_af_count = 0

        for key, value in speed_dict.items():
            recht_over_load = value[(value['Richting'] == 'Recht door') & (value['snelheid km/h'] >= r_spped)]
            af_over_load = value[((value['Richting'] == ' rechts af') | (value['Richting'] == ' links af'))
                                 & (value['snelheid km/h'] >= l_speed)]
            total_recht_count += len(value[value['Richting'] == 'Recht door'])
            total_af_count += len(value[(value['Richting'] == ' links af') | (value['Richting'] == ' rechts af')])
            recht_door_over_load_count += len(recht_over_load)
            af_over_load_count += len(af_over_load)
            to_frame_dict[key] = [len(recht_over_load) + len(af_over_load)]
        to_frame_dict['Recht door'] = [recht_door_over_load_count]
        to_frame_dict['Links/Rechts af'] = [af_over_load_count]
        to_frame_dict['Total recht'] = [total_recht_count]
        to_frame_dict['Total af'] = [total_af_count]
        total_df_list.append(pd.DataFrame(to_frame_dict))
    mixed_dict = {'all data': pd.concat(total_df_list).fillna(0)}
    save_to_sql('snelheid', mixed_dict, path='rapport')


if __name__ == '__main__':
    mix_speed(25, 20)
