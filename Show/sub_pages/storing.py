# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *

# streamlit
import streamlit as st
from Show.sub_pages.storing_mode.storingdata import st_storingdata
from Show.sub_pages.storing_mode.unknowstoring import st_unknowstoring
from Show.sub_pages.storing_mode.allstoring import st_all_storing
from Show.core import GetData


def st_storing():
    try:
        mode = st.sidebar.radio(
            'Grafiek mode：',
            (
                'Storing data', 'Unknow storing')#, 'All storing')
        )
        if mode == 'Storing data':
            all_table_name = GetData.get_data_name(path="storing")
            all_table_name.sort(reverse=True)
            default_table = all_table_name[:1]
            select_data = st.sidebar.multiselect(
                "Selecteer gegevens om te analyseren", all_table_name, default_table
            )
            # with Pool(len(select_data)) as p:
            #     p.map(st_storingdata, select_data)
            st_storingdata(select_data)
        elif mode == 'Unknow storing':
            all_table_name = GetData.get_data_name(path="unknow_storing")
            all_table_name.sort(reverse=True)
            default_table = all_table_name[:1]
            select_data = st.sidebar.multiselect(
                "Selecteer gegevens om te analyseren", all_table_name, default_table
            )
            st_unknowstoring(select_data)
        # elif mode == 'All storing':
        #     st_all_storing(select_data)
        # else:
        #     all_table_name = GetData.get_data_name(path="all_storing")
        #     all_table_name.sort(reverse=True)
        #     default_table = all_table_name[:1]
        #     select_data = st.sidebar.multiselect(
        #         "Selecteer gegevens om te analyseren", all_table_name, default_table
        #     )
        #     st_all_storing(select_data)
    except:
        st.title('Kies een gegeven om te analyseren')