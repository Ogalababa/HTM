# ！/usr/bin/python3
# coding:utf-8

from __init__ import *
import pandas as pd
import sqlalchemy
from Run.core.ConvertData.ConnectDB import conn_engine
from Run.core.Integration.DataInitialization import get_alldata_from_db

# streamlit
import streamlit as st
import base64


def get_data_name(path='db'):
    """
    :return: list
    """
    all_db_file = os.listdir(os.path.join(rootPath, 'DataBase', path))
    all_db_name = [i[:-3] for i in all_db_file if i[-3:] == '.db']

    return all_db_name


def get_tram_speed(selected_db, path='snelheid'):
    """

    :param selected_db: list
    :param path: str
    :return: DataFrame
    """
    data_list = []
    for i in selected_db:
        insp = sqlalchemy.inspect(conn_engine(i, path))
        lijn_nrs = insp.get_table_names()
        for lijn in lijn_nrs:
            data_list.append(pd.read_sql_table(lijn, conn_engine(i, path)))
    all_data = pd.concat(data_list)
    all_data.rename(columns={'<aanmelden> lijn': 'Lijn',
                             '<afmelden> wagen': 'Wagen Nr',
                             '<aanmelden> categorie': 'Categorie',
                             '<aanmelden> service': 'Service',
                             'wissel nr': 'Wissel Nr',
                             'hfk_in': 'Tijd'}, inplace=True)
    all_data = all_data.drop(all_data[all_data['snelheid km/h'] > 50].index)
    all_data['Wagen Nr'] = all_data['Wagen Nr'].astype(str)
    return all_data


@st.cache(allow_output_mutation=True)
def get_tram_speed_cache(selected_db, path='snelheid'):
    """

    :param selected_db: list
    :param path: str
    :return: DataFrame
    """
    data_list = []
    for i in selected_db:
        insp = sqlalchemy.inspect(conn_engine(i, path))
        lijn_nrs = insp.get_table_names()
        for lijn in lijn_nrs:
            data_list.append(pd.read_sql_table(lijn, conn_engine(i, path)))
    all_data = pd.concat(data_list)
    all_data.rename(columns={'<aanmelden> lijn': 'Lijn',
                             '<afmelden> wagen': 'Wagen Nr',
                             '<aanmelden> categorie': 'Categorie',
                             '<aanmelden> service': 'Service',
                             'wissel nr': 'Wissel Nr',
                             'hfk_in': 'Tijd'}, inplace=True)
    all_data = all_data.drop(all_data[all_data['snelheid km/h'] > 50].index)
    all_data['Wagen Nr'] = all_data['Wagen Nr'].astype(str)
    return all_data


def create_download_link(val, filename, pdf='pdf'):
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,' \
           f'{b64.decode()}" download="{filename}.{pdf}">Download {pdf.upper()}</a>'



def get_all_data(selected_db, path='db'):
    """
    Read all data from log db
    :param selected_db: list
    :param path: database dir
    :return: {wissel nr: Dataframe}
    """
    data_list = []
    wissel_list = []
    for i in selected_db:
        if f'{i}.db' in os.listdir(os.path.join(rootPath, 'DataBase', path)):
            data_dict = get_alldata_from_db(i, path=path)
            wissel_list.extend(data_dict.keys())
            data_list.append(data_dict)
    return data_list, list(set(wissel_list))


@st.cache(allow_output_mutation=True)
def get_all_data_cache(selected_db, path='db'):
    """
    Read all data from log db
    :param selected_db: list
    :param path: database dir
    :return: {wissel nr: Dataframe}
    """
    data_list = []
    wissel_list = []
    for i in selected_db:
        if f'{i}.db' in os.listdir(os.path.join(rootPath, 'DataBase', path)):
            data_dict = get_alldata_from_db(i, path=path)
            wissel_list.extend(data_dict.keys())
            data_list.append(data_dict)
    return data_list, list(set(wissel_list))