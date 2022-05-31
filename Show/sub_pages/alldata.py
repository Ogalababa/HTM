# ！/usr/bin/python3
# coding:utf-8
# sys

import streamlit as st

from Show.core.GetData import get_all_data
from Show.core.GetData import get_all_data_cache
from Show.core.GetData import get_data_name


def all_data():
    # get database file name
    # 获取数据库文件名
    all_table_name = get_data_name()
    all_table_name.sort(reverse=True)
    default_table = all_table_name[:1]
    select_data = st.sidebar.multiselect(
        "Selecteer gegevens om te analyseren", all_table_name, default_table
    )
    # website content
    layout_height = 600
    cache = st.sidebar.checkbox('Cache')
    if len(select_data) > 0:
        if cache:
            all_data_list, wissel_list = get_all_data_cache(select_data)
        else:
            all_data_list, wissel_list = get_all_data(select_data)
        wissel_list.sort()
        select_wissel = st.sidebar.selectbox('Kies een wissel', wissel_list)
        for i in all_data_list:
            st.dataframe(i.get(select_wissel), height=700)

    else:
        st.title('Kies een gegeven om te analyseren')
