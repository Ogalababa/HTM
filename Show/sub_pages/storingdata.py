# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
import pandas as pd
import streamlit as st
import plotly.express as px
from Show.core.GetData import get_all_data


def st_storingdata(select_data):
    layout_height = 600
    col2, space2, col3 = st.columns((10, 1, 10))
    col4, space4, col5 = st.columns((10, 1, 10))
    if len(select_data) > 0:
        all_data_list, wissel_list = get_all_data(select_data, path='storing')
        wissel_list.sort()
        select_wissel = st.sidebar.selectbox('Kies een wissel', wissel_list)
        for i in all_data_list:
            with col2:
                fig_storing_1 = px.sunburst(i.get(select_wissel),
                                            title='Storing overzicht',
                                            path=['storing', 'wissel nr', 'afdelling', 'begin tijd'],
                                            values='count',
                                            color='storing',
                                            color_continuous_scale=px.colors.sequential.RdBu,
                                            hover_data=['begin tijd', 'eind tijd'],
                                            height=layout_height)
                st.plotly_chart(fig_storing_1, use_container_width=True)
            with col3:
                fig_storing_1 = px.sunburst(i.get(select_wissel),
                                            title='Storing overzicht',
                                            path=['wissel nr', 'afdelling', 'storing', 'begin tijd'],
                                            values='count',
                                            color='storing',
                                            color_continuous_scale=px.colors.sequential.RdBu,
                                            hover_data=['begin tijd', 'eind tijd'],
                                            height=layout_height)
                st.plotly_chart(fig_storing_1, use_container_width=True)
            with col4:
                fig_storing_1 = px.sunburst(i.get(select_wissel),
                                            title='Storing overzicht',
                                            path=['afdelling', 'storing', 'wissel nr', 'begin tijd'],
                                            values='count',
                                            color='storing',
                                            color_continuous_scale=px.colors.sequential.RdBu,
                                            hover_data=['begin tijd', 'eind tijd'],
                                            height=layout_height)
                st.plotly_chart(fig_storing_1, use_container_width=True)
            with col5:
                loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
                wagen_loc = pd.merge(loc_df, i.get(select_wissel), on=['Wissel Nr'], how='inner')
                st.map(wagen_loc, zoom=10)
    else:
        st.title('Kies een gegeven om te analyseren')


def st_unknowstoring(select_data):
    layout_height = 600
    if len(select_data) > 0:
        all_data_list, wissel_list = get_all_data(select_data, path='unknow_storing')
        wissel_list.sort()
        select_wissel = st.sidebar.selectbox('Kies een wissel', wissel_list)
        for i in all_data_list:
            st.dataframe(i.get(select_wissel), height=1000)

    else:
        st.title('Kies een gegeven om te analyseren')