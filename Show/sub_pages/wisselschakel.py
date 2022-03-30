# ！/usr/bin/python3
# coding:utf-8
# sys

import pandas as pd
import plotly.express as px
import plotly.io as pio


# streamlit
import streamlit as st
from Show.core.GetData import get_tram_speed, create_download_link, get_all_data
from fpdf import FPDF
from tempfile import NamedTemporaryFile


def st_wissel_schakel(select_data):
    """
    Get wissl switch data display on streamlit
    :param select_data: database name in list
    :return: display on streamlit
    """
    layout_height = 600
    figs = []

    if len(select_data) > 0:
        # reset DataFrame
        data_dict_list, wissel_name_list = get_all_data(select_data, path='schakelen')
        dataframe_list = []
        for i in data_dict_list:
            dataframe_list.append(pd.concat(i.values()))
        all_data_df = pd.concat(dataframe_list)
        all_data_df['tijd'] = pd.to_datetime(all_data_df['tijd'])
        st.dataframe(all_data_df)

    else:
        st.title('Kies een gegeven om te analyseren')