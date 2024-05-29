# ！/usr/bin/python3
# coding:utf-8
# sys
from Show.sub_pages.Utils import generate_dates_within_last_month
from __init__ import *
import calendar
import datetime
import streamlit as st
from Show.core.GetData import create_download_link, get_tram_speed
from Show.sub_pages.rapport_mode.snelheid_rep import snelheid_rapport
from Show.sub_pages.rapport_mode.storing_rep import storing_rapport
from fpdf import FPDF
from tempfile import NamedTemporaryFile
import pandas as pd
import plotly.express as px
import plotly.io as pio


def speed_boxplot():
    # website content

    mode = st.sidebar.radio(
        "Periode", ("1 maand", '3 maanden', "6 maanden", "12 maanden")
    )
    if mode == '12 maand':
        dates = generate_dates_within_last_month(12)
    elif mode == '3 maanden':
        dates = generate_dates_within_last_month(3)
    elif mode == '6 maanden':
        dates = generate_dates_within_last_month(6)
    else:
        dates = generate_dates_within_last_month(1)

    df_all_data = get_tram_speed(dates)
    df_all_data = df_all_data[df_all_data['snelheid km/h'] > 5][['Wissel Nr', 'Richting', 'snelheid km/h']]
    df_rechtdoor = df_all_data[df_all_data['Richting'] == 'Recht door']
    df_af = df_all_data[df_all_data['Richting'] != 'Recht door']

    df_stats_rechtdoor = df_rechtdoor.groupby('Wissel Nr').agg({
        'snelheid km/h': ['min', 'max', lambda x: round(x.mean(), 2), 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]
    })

    df_stats_af = df_af.groupby('Wissel Nr').agg({
        'snelheid km/h': ['min', 'max', lambda x: round(x.mean(), 2), 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]
    })

    df_stats_rechtdoor.columns = ['Vmin', 'Vmax', 'Vgem', 'Median', 'Q1', 'Q3']
    df_stats_rechtdoor = df_stats_rechtdoor.reset_index()
    df_stats_rechtdoor['Richting'] = 'Rechtdoor'

    df_stats_af.columns = ['Vmin', 'Vmax', 'Vgem', 'Median', 'Q1', 'Q3']
    df_stats_af = df_stats_af.reset_index()
    df_stats_af['Richting'] = 'Afbuigen'

    df_merged = pd.concat([df_stats_rechtdoor, df_stats_af])

    # 重置索引
    df_merged = df_merged.reset_index(drop=True)

    # website content
    fig_rechtdoor = px.box(df_rechtdoor, x='Wissel Nr', y='snelheid km/h',
                           title="Box Plot van 'snelheid km/h' op 'Wissel Nr' richting 'Rechtdoor'")
    fig_af = px.box(df_rechtdoor, x='Wissel Nr', y='snelheid km/h',
                    title="Box Plot van 'snelheid km/h' op 'Wissel Nr' richting 'Afbuigen'")

    st.plotly_chart(fig_rechtdoor, use_container_width=True)
    st.plotly_chart(fig_af, use_container_width=True)
    st.dataframe(df_merged)

    # export csv
    export_as_csv = st.sidebar.button("Download Details")
    if export_as_csv:
        csv = df_merged.to_csv(index=False).encode()
        href = create_download_link(csv, f'boxplot_snelheid_{mode}_{datetime.date.today()}', 'csv')
        st.sidebar.markdown(href, unsafe_allow_html=True)
