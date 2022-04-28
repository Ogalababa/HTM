# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import pandas as pd
import streamlit as st
import plotly.express as px
from Show.core.GetData import get_all_data


def st_unknowstoring(select_data):
    layout_height = 600
    if len(select_data) > 0:
        all_data_list, wissel_list = get_all_data(select_data, path='unknow_storing')
        wissel_list.sort()
        select_wissel = st.sidebar.selectbox('Kies een wissel', wissel_list)
        for i in all_data_list:
            st.subheader(i.get(select_wissel)['wissel nr'].tolist()[0])
            st.dataframe(i.get(select_wissel), height=1000)

    else:
        st.title('Kies een gegeven om te analyseren')