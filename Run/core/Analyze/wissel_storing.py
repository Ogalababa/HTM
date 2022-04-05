# ！/usr/bin/python3
# coding:utf-8
# sys

import pandas as pd

def wissel_storing(df):
    """
    Calculate wissel storing from single wissel cycle
    :param df: sigle wissel cycle dataframe
    :return: wissel switch status dataframe
    """
    status = {}
    status['Begin tijd'] = [df.iloc[1]['date-time']]
    status['Eind tijd'] = [df.iloc[-1]['date-time']]
    status['Wissel nr'] = [df.iloc[-1]['wissel nr']]
    status['lijn'] = [df.iloc[-1]['<aanmelden> lijn']]
    status['service'] = [df.iloc[-1]['<aanmelden> service']]
    status['categorie'] = [df.iloc[-1]['<aanmelden> categorie']]
    status['wagen'] = [df.iloc[-1]['<aktuell> wagen']]
    desc = df.describe()
    status['fifo'] = [desc.loc['max']['<aktuell> niveau fifo']]

    if desc.loc['max']['<aktuell> wagen'] == 0:
        status['Error type'] = ['Wagen nummer aanmelden fout']
        status['Veroozak'] = ['Tram Vecom system']
        return pd.DataFrame(status)
    else:
        return -1

