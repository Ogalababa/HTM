# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import pandas as pd
import plotly.express as px


# streamlit
import streamlit as st


def fig_voertuigs(df_all_data, layout_height):
    col2, space2, col3 = st.columns((10, 1, 10))
    col4, space4, col5 = st.columns((10, 1, 10))
    col6, space6, col7 = st.columns((10, 1, 10))
    voertuig_list = list(set(df_all_data['voertuig Nr']))
    ex_list = list(map(str, range(1000)))
    # voertuig_list = [i for i in voertuig_list if i != '0']
    voertuig_list = [i for i in voertuig_list if i not in ex_list]
    voertuig_list.sort()
    selected_voertuig = st.sidebar.selectbox('Kies een voertuig', voertuig_list)
    df_all_data = df_all_data.set_index('voertuig Nr', drop=False)
    speed_counts = df_all_data.loc[selected_voertuig].copy()
    speed_counts['hoeveelheid'] = 1

    with col2:
        try:
            fig_voertuig_2 = px.bar(speed_counts.sort_values(by='snelheid km/h'),
                                 title='Wissel/snelheid overzicht',
                                 x='snelheid km/h', y='hoeveelheid',
                                 color='code',
                                 height=layout_height,
                                 hover_data=['Lijn',
                                             'Wissel Nr',
                                             'Categorie',
                                             'Service',
                                             'Tijd',
                                             'Richting'],
                                 color_continuous_scale=px.colors.sequential.Sunsetdark)
            st.plotly_chart(fig_voertuig_2, use_container_width=True)
        except:
            st.title('Geen Data')

    with col3:
        fig_voertuig = px.scatter(df_all_data.loc[selected_voertuig],
                               x='Tijd', y='snelheid km/h',
                               title='Wissel snelheid/tijd grafiek',
                               hover_data=['Lijn',
                                           'Wissel Nr',
                                           'Categorie',
                                           'Service',
                                           'Richting'],
                               color='code',
                               color_continuous_scale=px.colors.sequential.Sunsetdark,
                               size='snelheid km/h',
                               symbol='Richting',
                               height=layout_height,
                               )
        st.plotly_chart(fig_voertuig, use_container_width=True)

    with col4:
        speed_counts['Tijd'] = speed_counts['Tijd'].astype(str)
        fig_counts_2 = px.sunburst(speed_counts,
                                   title='Snelheid overzicht',
                                   path=['code', 'snelheid km/h', 'Richting', 'Wissel Nr'],
                                   values='hoeveelheid',
                                   color='snelheid km/h',
                                   color_continuous_scale=px.colors.sequential.RdBu,
                                   height=layout_height,
                                   hover_data=[
                                       'Categorie',
                                       'Service',
                                   ])
        fig_counts_2.update_traces(textinfo='label+percent entry')
        st.plotly_chart(fig_counts_2, use_container_width=True)

    with col5:
        fig_wissel_3 = px.pie(speed_counts,
                              values='hoeveelheid',
                              names='snelheid km/h',
                              title='Snelheid percentage',
                              color_discrete_sequence=px.colors.sequential.RdBu,
                              height=layout_height,
                              hole=.25,
                              )
        # fig_wissel_3.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_wissel_3, use_container_width=True)

    with col6:
        fig_wissel_5 = px.pie(speed_counts,
                              values='hoeveelheid',
                              names='Richting',
                              title='Richting percentage',
                              color_discrete_sequence=px.colors.sequential.RdBu,
                              height=layout_height,
                              hole=.25,
                              )
        # fig_wissel_5.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_wissel_5, use_container_width=True)

    with col7:
        loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
        voertuig_loc = pd.merge(loc_df, speed_counts, on=['Wissel Nr'], how='inner')
        # st.map(voertuig_loc, zoom=10)
        fig_7 = px.scatter_mapbox(voertuig_loc,
                                  lat="latitude", lon="longitude",
                                  color_discrete_sequence=px.colors.sequential.RdBu,
                                  height=layout_height, size_max=15, zoom=10, color='Wissel Nr',
                                  hover_data=['Wissel Nr'], mapbox_style="carto-positron")
        st.plotly_chart(fig_7)
