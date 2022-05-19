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
            fig_data = i.get(select_wissel)[i.get(select_wissel)['storing'] != 'wissel buiten dienst']
            st.dataframe(fig_data)
            with col4:
                fig_storing_1 = px.sunburst(fig_data,
                                            title='Storing overzicht',
                                            path=['storing', 'Wissel Nr', 'afdelling', 'wagen nr', 'begin tijd'], 
                                            values='count', 
                                            color='storing',
                                            color_continuous_scale=px.colors.sequential.RdBu,
                                            hover_data=['begin tijd', 'eind tijd', 'lijn nr', 'categorie', 'service', 'wagen nr'],
                                            height=layout_height,
                                            template='seaborn')
                st.plotly_chart(fig_storing_1, use_container_width=True)
            with col3:
                fig_storing_1 = px.sunburst(fig_data,
                                            title='Wissel overzicht',
                                            path=['wagen nr','afdelling','storing', 'Wissel Nr', 'begin tijd'], 
                                            values='count', 
                                            color='wagen nr',
                                            color_continuous_scale=px.colors.sequential.RdBu,
                                            hover_data=['begin tijd', 'eind tijd', 'lijn nr', 'categorie', 'service', 'wagen nr'],
                                            height=layout_height,
                                            template='seaborn')
                st.plotly_chart(fig_storing_1, use_container_width=True)
            with col2:
                fig_storing_1 = px.sunburst(fig_data,
                                            title='Afdelling overzicht',
                                            path=['afdelling', 'storing', 'Wissel Nr', 'wagen nr', 'begin tijd'], 
                                            values='count', 
                                            color='afdelling',
                                            color_continuous_scale=px.colors.sequential.RdBu,
                                            hover_data=['begin tijd', 'eind tijd', 'lijn nr', 'categorie', 'service', 'wagen nr'],
                                            height=layout_height,
                                            template='seaborn')
                st.plotly_chart(fig_storing_1, use_container_width=True)
            with col5:
                loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
                wagen_loc = pd.merge(loc_df, fig_data, on=['Wissel Nr'], how='inner')
                st.map(wagen_loc, zoom=10)
    else:
        st.title('Kies een gegeven om te analyseren')

