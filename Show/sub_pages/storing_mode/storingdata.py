# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import pandas as pd
import streamlit as st
import plotly.express as px
from Show.core.GetData import get_all_data


def pool_col(func):
    return func


def st_storingdata(select_data):
    layout_height = 600
    col2, space2, col3 = st.columns((10, 1, 10))
    col4, space4, col5 = st.columns((10, 1, 10))
    stop = st.sidebar.checkbox('Hoog niveau storing')
    if len(select_data) > 0:
        all_data_list, wissel_list = get_all_data(select_data, path='storing')
        wissel_list.sort()
        all_data_df_list = []
        for i in all_data_list:
            for key, values in i.items():
                all_data_df_list.append(values)
        fig_data_1 = pd.concat(all_data_df_list)
        fig_data_1 = fig_data_1[fig_data_1['storing'] != 'wissel buiten dienst']
        if stop:
            fig_data = fig_data_1[fig_data_1['wissel stop'] == 1]
        else:
            fig_data = fig_data_1
        fig_data['begin tijd'] = pd.to_datetime(fig_data['begin tijd'])
        fig_data['eind tijd'] = pd.to_datetime(fig_data['eind tijd'])
        fig_data = fig_data.reset_index(drop=True)
        st.dataframe(fig_data)

        with col2:
            # fig_storing_2 = px.pie(fig_data,
            #                        values='count',
            #                        names='afdelling',
            #                        title='Afdelling percentage',
            #                        color_discrete_sequence=px.colors.sequential.RdBu,
            #                        height=layout_height,
            #                        hole=.25,
            #                        template='seaborn'
            #                        )
            # fig_storing_2.update_traces(textinfo='percent+label')
            # st.plotly_chart(fig_storing_2, use_container_width=True)
            fig_storing_2 = px.sunburst(fig_data,
                                       title='afdelling',
                                       path=['afdelling', 'storing', 'begin tijd'],
                                       values='count',
                                       color='afdelling',
                                       color_continuous_scale=px.colors.sequential.RdBu,
                                       height=layout_height,
                                       hover_data=[
                                           'Wissel Nr',
                                           'lijn nr',
                                           'categorie',
                                           'wagen nr'
                                       ])
            fig_storing_2.update_traces(textinfo='label+percent entry')
            st.plotly_chart(fig_storing_2, use_container_width=True)
            

        with col3:
            fig_storing_4 = px.pie(fig_data,
                                   values='count',
                                   names='Wissel Nr',
                                   title='Wissel percentage',
                                   color_discrete_sequence=px.colors.sequential.RdBu,
                                   height=layout_height,
                                   hole=.25,
                                   template='seaborn'
                                   )
            fig_storing_4.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_storing_4, use_container_width=True)

        with col4:
            fig_storing_3 = px.pie(fig_data,
                                   values='count',
                                   names='storing',
                                   title='Storing percentage',
                                   color_discrete_sequence=px.colors.sequential.RdBu,
                                   height=layout_height,
                                   hole=.25,
                                   template='seaborn',
                                   )
            fig_storing_3.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_storing_3, use_container_width=True)

        with col5:
            loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
            wagen_loc = pd.merge(loc_df, fig_data, on=['Wissel Nr'], how='inner')
            # st.map(wagen_loc, zoom=10)
            fig_7 = px.scatter_mapbox(wagen_loc,
                                      lat="latitude", lon="longitude",
                                      color_discrete_sequence=px.colors.sequential.RdBu,
                                      height=layout_height, size_max=15, zoom=10, color='Wissel Nr',
                                      hover_data=['Wissel Nr'], mapbox_style="carto-positron")
            st.plotly_chart(fig_7)

    else:
        st.title('Kies een gegeven om te analyseren')

