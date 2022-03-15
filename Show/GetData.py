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
    all_db_file = os.listdir(os.path.join(rootPath, 'DataBase', path))
    all_db_name = [i[:-3] for i in all_db_file if i[-3:] == '.db']

    return all_db_name


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
