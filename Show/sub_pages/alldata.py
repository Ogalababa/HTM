# ！/usr/bin/python3
# coding:utf-8
# sys
import pandas as pd
import streamlit as st
from Show.core import GetData


def all_data(select_data):
    layout_height = 600
    if len(select_data) > 0:
        pass

    else:
        st.title('Kies een gegeven om te analyseren')