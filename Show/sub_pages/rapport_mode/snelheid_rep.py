# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import pandas as pd
import streamlit as st
import plotly.express as px
from Show.core.GetData import get_all_data, get_tram_speed
from Show.sub_pages.tramspeed_mode.max_waarde import max_waarde
import plotly.graph_objects as go


def snelheid_rapport(select_data, mode= 'week'):
    layout_height = 600
    col1, space1 = st.columns((21, 0.1))
    col2, space2, col3 = st.columns((10, 1, 10))
    col4, space4, col5 = st.columns((10, 1, 10))
    speed_data = get_tram_speed(select_data)
    if mode == 'month':
        speed_data['datum'] = 'week: ' + speed_data['Tijd'].dt.week.astype('str')
    elif mode == 'year':
        speed_data['datum'] = speed_data['Tijd'].dt.month
    else:
        speed_data['datum'] = pd.to_datetime(speed_data['Tijd']).dt.date
    speed_data['hoeveelheid'] = 1
    recht_door_speed = speed_data[(speed_data['Richting'] == 'Recht door') & (speed_data['snelheid km/h'] >= 25)]
    af_speed = speed_data[((speed_data['Richting'] == ' rechts af') | (speed_data['Richting'] == ' links af')) & (
                                            speed_data['snelheid km/h'] >= 20)]
    figs = []
    with col1:
        st.title('Snelheid rapport')
        st.sidebar.metric(f'Totale records boven 25 km/h:', len(recht_door_speed),
                          delta=f'{round(((len(recht_door_speed) / len(speed_data[speed_data["Richting"] == "Recht door"])) * 100), 3)}% van totale records',
                          delta_color="normal")
        st.sidebar.metric(f'Totale records boven 25 km/h:', len(af_speed),
                          delta=f'{round(((len(af_speed) / len(speed_data[(speed_data["Richting"] == " links af")|(speed_data["Richting"] == " rechts af")])) * 100), 3)}% van totale records',
                          delta_color="normal")
    with col2:
        recht_door = px.bar(
            speed_data[(speed_data['Richting'] == 'Recht door') & (speed_data['snelheid km/h'] >= 25)].sort_values(
                by='snelheid km/h'),
            title='Recht door snelheid boven 25km/h',
            x='datum', y='hoeveelheid', color='datum',
            hover_data=['snelheid km/h',
                        'Lijn',
                        'Wissel Nr',
                        'Categorie',
                        'Service',
                        'Tijd',
                        'Richting'
                        ],
            height=layout_height, color_continuous_scale=px.colors.sequential.Sunsetdark)
        st.plotly_chart(recht_door, use_container_width=True)
    with col3:
        af = px.bar(speed_data[((speed_data['Richting'] == ' rechts af') | (speed_data['Richting'] == ' links af')) & (
                                            speed_data['snelheid km/h'] >= 20)].sort_values(by='snelheid km/h'),
                            title='link/rechts af snelheid boven 20km/h',
                            x='datum', y='hoeveelheid', color='datum',
                            hover_data=['snelheid km/h',
                                        'Lijn',
                                        'Wissel Nr',
                                        'Categorie',
                                        'Service',
                                        'Tijd',
                                        'Richting'
                                        ],
                            height=layout_height, color_continuous_scale=px.colors.sequential.Sunsetdark)
        st.plotly_chart(af, use_container_width=True)
        
    return figs
