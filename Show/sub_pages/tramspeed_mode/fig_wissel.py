# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import pandas as pd
import plotly.express as px
# import plotly.io as pio

# streamlit
import streamlit as st
# from Show.core.GetData import get_tram_speed, create_download_link, get_data_name


def fig_wissel(df_all_data, layout_height):
    col2, space2, col3 = st.columns((10, 1, 10))
    col4, space4, col5 = st.columns((10, 1, 10))
    col6, space6, col7 = st.columns((10, 1, 10))

    wissel_list = list(set(df_all_data['Wissel Nr']))
    wissel_list.sort()
    selected_wissel = st.sidebar.selectbox('Kies een wissel', wissel_list)
    df_all_data = df_all_data.set_index('Wissel Nr', drop=False, )
    speed_counts_wissel = df_all_data.loc[selected_wissel].copy()
    speed_counts_wissel['hoeveelheid'] = 1
    with col2:
        fig_wissel_4 = px.bar(speed_counts_wissel.sort_values(by='snelheid km/h'),
                              title='Wagen/snelheid overzicht',
                              x='snelheid km/h', y='hoeveelheid',
                              color='code',
                              height=layout_height,
                              hover_data=['Lijn',
                                          'Wagen Nr',
                                          'Categorie',
                                          'Service',
                                          'Tijd',
                                          'Richting'],
                              color_continuous_scale=px.colors.sequential.Sunsetdark)
        st.plotly_chart(fig_wissel_4, use_container_width=True)
        # figs.append(fig_wissel_4)

    with col3:
        fig_wissel_1 = px.scatter(df_all_data.loc[selected_wissel],
                                  x='Tijd', y='snelheid km/h',
                                  title='Snelheid/tijd overzicht',
                                  hover_data=['Lijn',
                                              'Wagen Nr',
                                              'Categorie',
                                              'Service',
                                              'Richting'],
                                  color='code',
                                  color_continuous_scale=px.colors.sequential.Sunsetdark,
                                  size='snelheid km/h',
                                  symbol='Richting',
                                  height=layout_height,
                                  )
        st.plotly_chart(fig_wissel_1, use_container_width=True)
        # figs.append(fig_wissel_1)

    with col4:
        speed_counts_wissel['Tijd'] = speed_counts_wissel['Tijd'].astype(str)
        fig_counts = px.sunburst(speed_counts_wissel,
                                 title='Snelheid overzicht',
                                 path=['snelheid km/h', 'Richting', 'code'],
                                 values='hoeveelheid',
                                 color='snelheid km/h',
                                 color_continuous_scale=px.colors.sequential.RdBu,
                                 height=layout_height,
                                 hover_data=[
                                     'Categorie',
                                     'Service',
                                     'Richting'
                                 ])
        fig_counts.update_traces(textinfo='label+percent entry')
        st.plotly_chart(fig_counts, use_container_width=True)
        # figs.append(fig_counts)

    with col5:
        fig_wissel_2 = px.pie(speed_counts_wissel,
                              values='hoeveelheid',
                              names='snelheid km/h',
                              title='Snelheid percentage',
                              color_discrete_sequence=px.colors.sequential.RdBu,
                              height=layout_height,
                              hole=.25,
                              )
        # fig_wissel_2.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_wissel_2, use_container_width=True)
        # figs.append(fig_wissel_2)

    with col6:
        fig_wissel_4 = px.pie(speed_counts_wissel,
                              values='hoeveelheid',
                              names='Richting',
                              title='Richting percentage',
                              color_discrete_sequence=px.colors.sequential.RdBu,
                              height=layout_height,
                              hole=.25,
                              )
        # fig_wissel_4.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_wissel_4, use_container_width=True)
        # figs.append(fig_wissel_4)
    with col7:
        loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
        # st.map(loc_df[loc_df['Wissel Nr'] == selected_wissel], zoom=10)
        fig_7 = px.scatter_mapbox(loc_df[loc_df['Wissel Nr'] == selected_wissel],
                                  lat="latitude", lon="longitude",
                                  color_discrete_sequence=px.colors.sequential.RdBu,
                                  height=layout_height, size_max=15, zoom=13, color='Wissel Nr',
                                  hover_data=['Wissel Nr'], mapbox_style="carto-positron")
        st.plotly_chart(fig_7)
        # figs.append(fig_7)