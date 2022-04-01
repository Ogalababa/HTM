# ！/usr/bin/python3
# coding:utf-8
# sys

import pandas as pd
import plotly.express as px
import plotly.io as pio

# streamlit
import streamlit as st
from Show.core.GetData import get_tram_speed, create_download_link, get_all_data
from fpdf import FPDF
from tempfile import NamedTemporaryFile


def st_wissel_schakel(select_data):
    """
    Get wissl switch data display on streamlit
    :param select_data: database name in list
    :return: display on streamlit
    """
    layout_height = 600
    figs = []

    if len(select_data) > 0:
        # set page layout
        col2, space2, col3, = st.columns((17, 1, 3))
        col4, space4, col5 = st.columns((10, 1, 10))
        col6, space6, col7 = st.columns((10, 1, 10))
        # reset DataFrame
        data_dict_list, wissel_name_list = get_all_data(select_data, path='schakelen')
        dataframe_list = []
        for i in data_dict_list:
            dataframe_list.append(pd.concat(i.values()))
        all_data_df = pd.concat(dataframe_list)
        all_data_df['Tijd'] = pd.to_datetime(all_data_df['Tijd'])

        wissel_list = list(set(all_data_df['Wissel Nr']))
        wissel_list.sort()
        selected_wissel = st.sidebar.selectbox('Kies een wissel', wissel_list)
        schakel_data = all_data_df[all_data_df['Wissel Nr'] == selected_wissel]

        with col2:
            fig_schakelen_1 = px.line(
                schakel_data, x='Tijd', y='Na', title='Wissel schakelen overzicht',
                hover_data=['Wagen Nr', 'Voor', 'aanvragen', 'Na', 'Steps'], height=layout_height,
                markers=True
            )
            st.plotly_chart(fig_schakelen_1, use_container_width=True)
            figs.append(fig_schakelen_1)

        with col3:
            schakelen_value = schakel_data['Schakelen'].value_counts().to_dict()
            if 1 in schakelen_value.keys():
                aantalen = schakelen_value.get(1)
            else:
                aantalen = 0
            if -1 in schakelen_value.keys():
                storing = schakelen_value.get(-1)
            else:
                storing = 0
            schakel_delta = round((aantalen / len(schakel_data)) * 100)
            storing_delta = round((storing / len(schakel_data)) * 100)
            st.markdown('#')
            st.markdown('#')
            st.markdown('#')
            col3.metric("Aanvraag ", len(schakel_data))
            col3.metric("Overschakelen", aantalen, f'{schakel_delta} %')
            col3.metric("Storing", storing, f'{-storing_delta} %')

    else:
        st.title('Kies een gegeven om te analyseren')
