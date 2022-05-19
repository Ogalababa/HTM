# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *

# streamlit
import streamlit as st
from Show.sub_pages.storing_mode.storingdata import st_storingdata
from Show.sub_pages.storing_mode.unknowstoring import st_unknowstoring
from Show.sub_pages.storing_mode.allstoring import st_all_storing


def st_storing(select_data):
    mode = st.sidebar.radio(
        'Grafiek mode：',
        (
            'Storing data', 'Unknow storing', 'All storing')
    )
    if mode == 'Storing data':
        st_storingdata(select_data)
    elif mode == 'Unknow storing':
        st_unknowstoring(select_data)
    # elif mode == 'All storing':
    #     st_all_storing(select_data)
    else:
        st_all_storing(select_data)