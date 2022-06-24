# ！/usr/bin/python3
# coding:utf-8
# sys
from Show.core import GetData
from __init__ import *
import pandas as pd
import plotly.express as px

# streamlit
import streamlit as st
from Show.core.GetData import get_all_data, get_data_name
from Show.core.GetData import get_all_data_cache
from Show.core.GetData import create_download_link
from fpdf import FPDF
from tempfile import NamedTemporaryFile


def st_wissel_schakel():
    """
    Get wissl switch data display on streamlit
    :param select_data: database name in list
    :return: display on streamlit
    """
    # get database file name
    # 获取数据库文件名
    all_table_name = get_data_name(path="schakelen")
    all_table_name.sort(reverse=True)
    default_table = all_table_name[:1]
    select_data = st.sidebar.multiselect(
        "Selecteer gegevens om te analyseren", all_table_name, default_table
    )
    
    # website content
    layout_height = 600
    figs = []
    cache = st.sidebar.checkbox('Cache')
    if len(select_data) > 0:
        # set page layout
        col2, col3, = st.columns((17, 3))
        col4, space4, col5 = st.columns((10, 1, 10))
        col6, space6, col7 = st.columns((10, 1, 10))
        # reset DataFrame
        if cache:
            data_dict_list, wissel_name_list = get_all_data_cache(select_data, path='schakelen')
        else:
            data_dict_list, wissel_name_list = get_all_data(select_data, path='schakelen')
        dataframe_list = []
        for i in data_dict_list:
            dataframe_list.append(pd.concat(i.values()))
        all_data_df = pd.concat(dataframe_list)
        # all_data_df['Tijd'] = pd.to_datetime(all_data_df['Tijd'])
        
        wissel_list = list(set(all_data_df['Wissel Nr']))
        wissel_list.sort()
        selected_wissel = st.sidebar.selectbox('Kies een wissel', wissel_list)
        schakel_data = all_data_df[all_data_df['Wissel Nr'] == selected_wissel]
        
        with col2:
            fig_schakelen_1 = px.line(schakel_data,
                                      x='Tijd', y='Na',
                                      title=f'Wissel {selected_wissel} omstel beweging overzicht',
                                      hover_data=['Wagen Nr',
                                                  'Voor',
                                                  'aanvragen',
                                                  'Na',
                                                  'Steps'],
                                      height=layout_height,
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
            st.subheader(selected_wissel)
            col3.metric("Aanvraag ", len(schakel_data), )
            col3.metric("Omstel beweging", aantalen, f'{schakel_delta} %')
            col3.metric("Storing", storing, f'{-storing_delta} %')
            if storing_delta > 50:
                st.error('Incorrecte data')
        # with col4:
        #     loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
        #     st.map(loc_df[loc_df['Wissel Nr'] == selected_wissel], zoom=10)
        with col4:
           
            loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
            fig_5 = px.scatter_mapbox(loc_df[loc_df['Wissel Nr'] == selected_wissel], 
                                      lat="latitude", lon="longitude",
                                      color_continuous_scale=px.colors.sequential.RdBu, 
                                      height=layout_height, size_max=15, zoom=13, 
                                      hover_data=['Wissel Nr'],mapbox_style="carto-positron")
            st.plotly_chart(fig_5)
        # export_as_pdf = st.sidebar.button("Download Rapport")
        # export_as_csv = st.sidebar.button("Download Details")
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
        # if export_as_csv:
        #     csv = all_data_df.to_csv(index=False).encode()
        #     if len(select_data) >= 2:
        #         href = create_download_link(csv, f'{mode}-{select_data[-1]}_{select_data[0]}', 'csv')
        #     else:
        #         href = create_download_link(csv, f'{mode}-{select_data[0]}', 'csv')
        #     st.sidebar.markdown(href, unsafe_allow_html=True)

    else:
        st.title('Kies een gegeven om te analyseren')