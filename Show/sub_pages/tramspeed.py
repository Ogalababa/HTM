# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
# import pandas as pd
# import plotly.express as px
# import plotly.io as pio

# streamlit
import streamlit as st
from Show.core.GetData import get_tram_speed, create_download_link, get_data_name
# from fpdf import FPDF
# from tempfile import NamedTemporaryFile

# website index
from Show.sub_pages.tramspeed_mode.max_waarde import max_waarde
from Show.sub_pages.tramspeed_mode.fig_wissel import fig_wissel
from Show.sub_pages.tramspeed_mode.fig_wagen import fig_wagens
from Show.sub_pages.tramspeed_mode.fig_lijn import fig_lijn
from Show.sub_pages.tramspeed_mode.waarschuwing import waarschuwing
from Show.sub_pages.tramspeed_mode.fig_rit import fig_rit


def tram_speed():
    # get database file name
    # 获取数据库文件名
    # try:
    all_table_name = get_data_name(path="snelheid")
    all_table_name.sort(reverse=True)
    default_table = all_table_name[1]
    select_data = st.sidebar.multiselect(
        "Selecteer gegevens om te analyseren", all_table_name, default_table
    )

    # website content
    layout_height = 600
    figs = []
    # cache = st.sidebar.checkbox('Cache')
    if len(select_data) > 0:
        # if cache:
        #     df_all_data = get_tram_speed_cache(select_data)
        # else:
        #     df_all_data = get_tram_speed(select_data)
        df_all_data = get_tram_speed(select_data)
        speed_record_size = len(df_all_data)
        mode = st.sidebar.radio(
            'Grafiek mode：',
            (
            'Snelheidswaarschuwing', 'Max waarde', 'Grafiek per wissel', 'Grafiek per wagen', 'Grafiek per lijn', 'Grafiek per rit(Beta)')
        )
        if mode == 'Max waarde':
            fig_max = max_waarde(df_all_data)
            figs.append(fig_max)

        elif mode == 'Grafiek per wissel':
            fig_wissel(df_all_data, layout_height)

        elif mode == 'Grafiek per wagen':
            fig_wagens(df_all_data, layout_height)

        elif mode == 'Snelheidswaarschuwing':
            waarschuwing(df_all_data, speed_record_size, layout_height)
        elif mode == 'Grafiek per rit(Beta)':
            rit_data = fig_rit(layout_height)

        else:
            fig_lijn(df_all_data, layout_height)

        # export_as_pdf = st.sidebar.button("Download Rapport")
        export_as_csv = st.sidebar.button("Download Details")
        # if export_as_pdf:
        #     pdf = FPDF()
        #     for fig in figs:
        #         pdf.add_page(orientation='L')
        #         with NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
        #             pio.write_image(fig, tmpfile.name, height=500)
        #             pdf.image(tmpfile.name, 10, 10)
        #     if len(select_data) >= 2:
        #         html = create_download_link(pdf.output(dest="S").encode("latin-1"),
        #                                     f'{mode}_{select_data[-1]}_{select_data[0]}')
        #     else:
        #         html = create_download_link(pdf.output(dest="S").encode("latin-1"),
        #                                     f'{mode}-{select_data[0]}')
        #     st.sidebar.markdown(html, unsafe_allow_html=True)
        if export_as_csv:
            if mode == 'Grafiek per rit(Beta)':
                csv = rit_data.to_csv(index=False).encode()
                href = create_download_link(csv, f'{mode}', 'csv')
                
            else:
                csv = df_all_data[[
                    'Wagen Nr', 'Lijn', 'Service',
                    'Categorie', 'Wissel Nr', 'Tijd',
                    'snelheid km/h', 'Richting']].sort_values(by=['snelheid km/h']).to_csv(index=False).encode()
                if len(select_data) >= 2:
                    href = create_download_link(csv, f'{mode}-{select_data[-1]}_{select_data[0]}', 'csv')
                else:
                    href = create_download_link(csv, f'{mode}-{select_data[0]}', 'csv')
            st.sidebar.markdown(href, unsafe_allow_html=True)

    else:
        st.title('Kies een gegeven om te analyseren')
    # except:
    #     st.title('Geen data beschikbaar')