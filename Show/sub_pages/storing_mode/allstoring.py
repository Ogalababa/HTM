# ！/usr/bin/python3
# coding:utf-8
# sys

import streamlit as st
from Show.core.GetData import get_all_data
from Show.core.GetData import get_all_data_cache


def st_all_storing(select_data):
    layout_height = 600
    cache = st.sidebar.checkbox('Cache')
    if len(select_data) > 0:
        if cache:
            all_data_list, wissel_list = get_all_data_cache(select_data, path='all_storing')
        else:
            all_data_list, wissel_list = get_all_data(select_data, path='all_storing')
        wissel_list.sort()
        select_wissel = st.sidebar.selectbox('', wissel_list)
        for i in all_data_list:
            st.dataframe(i.get(select_wissel), height=700)

    else:
        st.title('Kies een gegeven om te analyseren')
