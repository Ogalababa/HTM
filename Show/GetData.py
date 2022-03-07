# ！/usr/bin/python3
# coding:utf-8

from __init__ import *
import pandas as pd
import sqlalchemy
from DataBase.ConnectDB import conn_engine

# streamlit
import streamlit as st
import base64


def get_data_name(path='db'):
    """
    :return: list
    """
    all_db_file = os.listdir(os.path.join(rootPath, 'HTM', '../DataBase', path))
    all_db_name = [i[:-3] for i in all_db_file if i[-3:] == '.db']

    return all_db_name


@st.cache
def get_sql_wissel_nr(selected_db):
    """
    :param selected_db: str
    :return: DataFrame
    """
    data_list = []
    for i in selected_db:
        insp = sqlalchemy.inspect(conn_engine(i))
        all_wissels = insp.get_table_names()
        for wissel_nr in all_wissels:
            data_list.append(pd.read_sql_table(wissel_nr, conn_engine(i), columns=['wissel nr']))
    all_data = pd.concat(data_list)

    return all_data


@st.cache
def get_sql_wissel_time(selected_db):
    """

    :param selected_db: list
    :return: DataFrame
    """
    data_list = []
    for i in selected_db:
        insp = sqlalchemy.inspect(conn_engine(i))
        all_wissels = insp.get_table_names()
        for wissel_nr in all_wissels:
            data_list.append(pd.read_sql_table(wissel_nr, conn_engine(i),
                                               columns=['date-time', 'time', 'server time', 'wissel nr']))
    all_data = pd.concat(data_list)
    try:
        all_data['date-time'] = pd.to_datetime(all_data['date-time'])
        all_data.set_index('date-time')
    except ValueError:
        pass

    return all_data


@st.cache
def get_sql_data_with_nr(selected_db, wissel_nr, paths='db'):

    """
    :param paths: str
    :param selected_db: list
    :param wissel_nr: str
    :return: DataFrame
    """

    data_list = []
    for i in selected_db:
        data_list.append(pd.read_sql_table(wissel_nr, conn_engine(i, path=paths)))
    all_data = pd.concat(data_list)
    all_data.reset_index(drop=True, inplace=True)
    return all_data


@st.cache
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
    all_data = all_data.drop(all_data[all_data['snelheid km/h'] > 60].index)
    all_data['Wagen Nr'] = all_data['Wagen Nr'].astype(str)
    return all_data


def create_download_link(val, filename, pdf='pdf'):
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,' \
           f'{b64.decode()}" download="{filename}.{pdf}">Download {pdf.upper()}</a>'
