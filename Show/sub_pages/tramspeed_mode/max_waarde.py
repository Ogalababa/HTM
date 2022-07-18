# ！/usr/bin/python3
# coding:utf-8
# sys


import pandas as pd
import plotly.express as px


# streamlit
import streamlit as st


def max_col2(df_all_data):
    wissel_base = df_all_data.set_index('Wissel Nr', drop=False, inplace=False).sort_index()
    fig_max_wissel = px.bar(wissel_base.groupby(
        pd.Grouper(key='Wissel Nr')).max().rename_axis(
        'Wissel Nr').reset_index().sort_values(by='snelheid km/h'),
                            title='Max snelheid per wissel',
                            x='Wissel Nr', y='snelheid km/h',
                            color='snelheid km/h',
                            color_continuous_scale=px.colors.sequential.Reds)
    st.plotly_chart(fig_max_wissel, use_container_width=True)
    return fig_max_wissel


def max_col3(df_all_data):
    voertuig_base = df_all_data.set_index('voertuig Nr', drop=False, inplace=False).sort_index()
    fig_max_voertuig = px.bar(voertuig_base.groupby(
        pd.Grouper(key='voertuig Nr')).max().rename_axis(
        'voertuig Nr').reset_index().sort_values(by='snelheid km/h'),
                           title='Max snelheid per voertuig',
                           x='voertuig Nr', y='snelheid km/h',
                           color='snelheid km/h',
                           color_continuous_scale=px.colors.sequential.Blues)
    st.plotly_chart(fig_max_voertuig, use_container_width=True)
    return fig_max_voertuig
    
    
def max_col4(df_all_data):
    wissel_base = df_all_data.set_index('Wissel Nr', drop=False, inplace=False).sort_index()
    fig_mean_wissel = px.bar(wissel_base.groupby(
        pd.Grouper(key='Wissel Nr')).mean().round(0).rename_axis(
        'Wissel Nr').reset_index().sort_values(by='snelheid km/h'),
                             title='Gemiddeld snelheid per wissel',
                             x='Wissel Nr', y='snelheid km/h',
                             color='snelheid km/h',
                             color_continuous_scale=px.colors.sequential.Burg)
    st.plotly_chart(fig_mean_wissel, use_container_width=True)
    return fig_mean_wissel
    
    
def max_col5(df_all_data):
    voertuig_base = df_all_data.set_index('voertuig Nr', drop=False, inplace=False).sort_index()
    fig_mean_voertuig = px.bar(voertuig_base.groupby(
        pd.Grouper(key='voertuig Nr')).mean().round(0).rename_axis(
        'voertuig Nr').reset_index().sort_values(by='snelheid km/h'),
                            title='Gemiddeld snelheid per voertuig',
                            x='voertuig Nr', y='snelheid km/h',
                            color='snelheid km/h',
                            color_continuous_scale=px.colors.sequential.dense)
    st.plotly_chart(fig_mean_voertuig, use_container_width=True)
    return fig_mean_voertuig
    
    
def max_waarde(df_all_data):
    col2, space2, col3 = st.columns((10, 1, 10))
    col4, space4, col5 = st.columns((10, 1, 10))
    figs = []

    with col2:
        fig_max_wissel = max_col2(df_all_data)
        figs.append(fig_max_wissel)

    with col3:
        fig_max_voertuig = max_col3(df_all_data)
        figs.append(fig_max_voertuig)

    with col4:
        fig_mean_wissel = max_col4(df_all_data)
        figs.append(fig_mean_wissel)

    with col5:
        fig_mean_voertuig = max_col5(df_all_data)
        figs.append(fig_mean_voertuig)
    return figs