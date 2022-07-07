# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import pandas as pd
import streamlit as st
import plotly.express as px
from Show.core.GetData import st_get_alldata_from_db


def snelheid_rapport(select_data: list, mode='week'):
    layout_height = 600
    col1, space1 = st.columns((21, 0.1))
    col2, space2, col3 = st.columns((10, 1, 10))
    col4, space4, col5 = st.columns((10, 1, 10))
    speed_data = st_get_alldata_from_db('snelheid', path='rapport').get('all data')
    speed_data = speed_data[speed_data['datum'].isin(select_data)]
    
    if mode == 'month':
        speed_data['datum'] = pd.to_datetime(speed_data['datum'])
        speed_data['datum'] = 'week: ' + speed_data['datum'].dt.week.astype('str')
    elif mode == 'year':
        speed_data['datum'] = pd.to_datetime(speed_data['datum'])
        speed_data['datum'] = speed_data['datum'].dt.month_name()
    else:
        pass

    # set datas
    recht_door_speed = speed_data[['datum', 'Recht door']]
    af_speed = speed_data[['datum', 'Links/Rechts af']]

    # wissel counting
    wissel_nr_list = list(speed_data.columns)
    wissel_nr_list = [i for i in wissel_nr_list if 'W' in i]
    wissel_overspeed_dict = {}
    wissel_speed_list = []
    for i in wissel_nr_list:
        wissel_speed_list.append(speed_data[i].sum())
    wissel_speed_df = pd.DataFrame(list(zip(wissel_nr_list, wissel_speed_list)),
                                   columns=['Wissel Nr', 'hoeveelheid']).sort_values(by='hoeveelheid', ascending=False)

    figs = []
    with col1:
        title = st.title(f'Overbelast snelheid overzicht van {select_data[0]} tot {select_data[-1]}')
        # figs.append(title)
    with col2:
        recht_door = px.bar(
            recht_door_speed,
            title='Recht door snelheid boven 25km/h',
            x='datum', y='Recht door', color='datum',
            height=layout_height, color_continuous_scale=px.colors.sequential.Sunsetdark)
        st.plotly_chart(recht_door, use_container_width=True)
        figs.append(recht_door)
    with space2:
        met_recht = st.sidebar.metric(f'Totale records boven 25 km/h', recht_door_speed['Recht door'].sum(),
                  delta=f"{round((recht_door_speed['Recht door'].sum() / speed_data['Total recht'].sum()) * 100, 3)}\
                  % van totale records", delta_color="normal")
        met_af = st.sidebar.metric(f'Totale records boven 20 km/h', af_speed['Links/Rechts af'].sum(),
                         delta=f"{round((af_speed['Links/Rechts af'].sum() / speed_data['Total af'].sum()) * 100, 3)}\
                          % van totale records", delta_color="normal")
        # figs.append(met_recht)
        # figs.append(met_af)
    with col3:
        af = px.bar(
            af_speed,
            title='Links/Rechts af snelheid boven 20km/h',
            x='datum', y='Links/Rechts af', color='datum',
            height=layout_height, color_continuous_scale=px.colors.sequential.Sunsetdark)
        st.plotly_chart(af, use_container_width=True)
        figs.append(af)

    with col4:
        top_wissel = px.bar(wissel_speed_df.head(10),
                            title='Het meest overbelast wissels',
                            x='Wissel Nr', y='hoeveelheid', color='Wissel Nr',text_auto='.2s',
                            height=layout_height, color_continuous_scale=px.colors.sequential.Sunsetdark)
        top_wissel.update_traces(textfont_size=15, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(top_wissel, use_container_width=True)
        figs.append(top_wissel)
    with col5:
        loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
        wagen_loc = pd.merge(loc_df, wissel_speed_df.head(10), on=['Wissel Nr'], how='inner')
        # st.map(wagen_loc, zoom=10)
        fig_7 = px.scatter_mapbox(wagen_loc,
                                  lat="latitude", lon="longitude",
                                  color_discrete_sequence=px.colors.sequential.RdBu,
                                  height=layout_height, size_max=15, zoom=10, color='Wissel Nr',
                                  hover_data=['Wissel Nr'], mapbox_style="carto-positron")
        st.plotly_chart(fig_7)
        # figs.append(fig_7)
        
    return figs
