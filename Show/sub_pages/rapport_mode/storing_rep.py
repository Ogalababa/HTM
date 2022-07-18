# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import pandas as pd
import streamlit as st
import plotly.express as px
from Show.core.GetData import st_get_alldata_from_db


def storing_rapport(select_data: list, mode='week'):
    layout_height = 600
    col1, space1 = st.columns((21, 0.1))
    col2, space2, col2_1 = st.columns((10, 1, 10))
    col3, space3, col3_1 = st.columns((10, 1, 10))
    col4, space4, col4_1 = st.columns((10, 1, 10))
    col5, space5, col5_1 = st.columns((10, 1, 10))
    col6, space6, col6_1 = st.columns((10, 1, 10))
    col7, space7 = st.columns((20, 1))
    # 获取数据
    storing_data_raw = st_get_alldata_from_db('storing', path='rapport').get('all data')
    storing_data_raw = storing_data_raw[storing_data_raw['datum'].isin(select_data)]

    # 筛选数据
    storing_data_raw = storing_data_raw[storing_data_raw['wissel stop'] == 1]
    # 预处理数据
    storing_data = storing_data_raw[storing_data_raw['storing'] != 'wissel buiten dienst']
    storing_data = storing_data.sort_values('datum')
    storing_data['datum'] = pd.to_datetime(storing_data['datum'])
    # storing_data['begin tijd'] = pd.to_datetime(storing_data['begin tijd'])
    # storing_data['eind tijd'] = pd.to_datetime(storing_data['eind tijd'])
    # storing_data['looptijd'] = storing_data['eind tijd'] - storing_data['begin tijd']
    storing_data['week'] = 'week:' + storing_data['datum'].dt.week.astype('str')
    storing_data['maand'] = storing_data['datum'].dt.year.astype('str') + '-' + \
                            storing_data['datum'].dt.month.astype('str')
    storing_data['jaar'] = storing_data['datum'].dt.year.astype('str')
    storing_data['datum'] = storing_data['datum'].dt.date
    storing_data = storing_data.set_index(['jaar', 'maand', 'week', 'datum',
                                           'Wissel Nr', 'wagen nr', 'afdelling',
                                           'storing'])
    storing_data = storing_data.rename(columns={'count': 'hoeveelheid'})
    # 调整时间格式
    if mode == 'maand':
        counter = 'week'
    elif mode == 'jaar':

        counter = 'maand'
    else:
        counter = 'datum'

    figs = []
    with col1:
        st.title(f'Storing overzicht van {select_data[0]} tot {select_data[-1]}')
    # st.dataframe(storing_data.reset_index(drop=False))

    with col2:
        total_storing_df = pd.DataFrame(storing_data.count(level=counter))
        total_storing = px.bar(
            total_storing_df,
            title='Total storingen overzicht', text_auto=True,
            x=total_storing_df.index, y='hoeveelheid', color=total_storing_df.index,
            height=layout_height, color_continuous_scale=px.colors.sequential.Sunsetdark,
        )
        total_storing.update_traces(textfont_size=15, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(total_storing, use_container_width=True)
        figs.append(total_storing)

    with col2_1:
        total_storing_pie = px.sunburst(
            storing_data.reset_index(drop=False),
            title='Total storingen percentage',
            path=['afdelling', 'storing', 'begin tijd'],
            color_continuous_scale=px.colors.sequential.RdBu,
            height=layout_height,
            hover_data=[
                'Wissel Nr',
                'lijn nr',
                'categorie',
                'wagen nr'
            ],
            # template='seaborn'
        )
        total_storing_pie.update_traces(textinfo='label+percent entry')
        st.plotly_chart(total_storing_pie, use_container_width=True)

    with col3:
        afdelling_count = storing_data.groupby(level='afdelling').sum()
        afdelling = px.bar(afdelling_count,
                           title='Storing per afdelling overzicht', text_auto=True,
                           x=afdelling_count.index, y='hoeveelheid', color=afdelling_count.index,
                           height=layout_height, color_continuous_scale=px.colors.sequential.Sunsetdark)
        afdelling.update_traces(textfont_size=15, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(afdelling, use_container_width=True)
        figs.append(afdelling)

    with col3_1:
        afdelling_pie = px.pie(
            storing_data.reset_index(drop=False),
            title='Storingen per afdelling percentage',
            values='hoeveelheid',
            names='afdelling',
            color_discrete_sequence=px.colors.sequential.RdBu,
            height=layout_height,
            hole=.25,
            # template='seaborn'
        )
        afdelling_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(afdelling_pie, use_container_width=True)

    with col4:
        storing_afdelling = storing_data.groupby(level=['afdelling', 'storing']).sum()
        storing_afdelling = storing_afdelling.reset_index(drop=False)
        afdelling_bestuurder = px.bar(storing_afdelling[storing_afdelling['afdelling'] == 'bestuurder'],
                                      title='Storing door bestuurder overzicht', text_auto=True,
                                      x='storing', y='hoeveelheid', color='storing',
                                      height=layout_height, color_continuous_scale=px.colors.sequential.Sunsetdark)
        afdelling_bestuurder.update_traces(textfont_size=15, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(afdelling_bestuurder, use_container_width=True)
        figs.append(afdelling_bestuurder)

    with col4_1:
        storing_afdelling_pie = px.pie(
            storing_afdelling[storing_afdelling['afdelling'] == 'bestuurder'],
            title='Storing door bestuurder percentage',
            values='hoeveelheid',
            names='storing',
            color_discrete_sequence=px.colors.sequential.RdBu,
            height=layout_height,
            hole=.25,
            # template='seaborn'
        )
        storing_afdelling_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(storing_afdelling_pie, use_container_width=True)

    with col5:
        afdelling_infra = px.bar(storing_afdelling[storing_afdelling['afdelling'] == 'infra'],
                                 title='Storing door infra overzicht', text_auto=True,
                                 x='storing', y='hoeveelheid', color='storing',
                                 height=layout_height, color_continuous_scale=px.colors.sequential.Sunsetdark)
        afdelling_infra.update_traces(textfont_size=15, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(afdelling_infra, use_container_width=True)
        figs.append(afdelling_infra)

    with col5_1:
        afdelling_infra_pie = px.pie(
            storing_afdelling[storing_afdelling['afdelling'] == 'infra'],
            title='Storing door infra percentage',
            values='hoeveelheid',
            names='storing',
            color_discrete_sequence=px.colors.sequential.RdBu,
            height=layout_height,
            hole=.25,
            # template='seaborn'
        )
        afdelling_infra_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(afdelling_infra_pie, use_container_width=True)

    with col6:
        afdelling_wagen = px.bar(storing_afdelling[storing_afdelling['afdelling'] == 'wagen'],
                                 title='Storing door wagen overzicht', text_auto=True,
                                 x='storing', y='hoeveelheid', color='storing',
                                 height=layout_height, color_continuous_scale=px.colors.sequential.Sunsetdark)
        afdelling_wagen.update_traces(textfont_size=15, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(afdelling_wagen, use_container_width=True)
        figs.append(afdelling_wagen)

    with col6_1:
        loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
        wagen_loc = pd.merge(loc_df, storing_data_raw[storing_data_raw['storing'] == 'wissel buiten dienst'],
                             on=['Wissel Nr'], how='inner')
        # st.map(wagen_loc, zoom=10)
        fig_7 = px.scatter_mapbox(wagen_loc,
                                  title='Wissel buitendienst',
                                  lat="latitude", lon="longitude",
                                  color_discrete_sequence=px.colors.sequential.RdBu,
                                  height=layout_height, size_max=15, zoom=10, color='Wissel Nr',
                                  hover_data=['Wissel Nr', 'datum'], mapbox_style="carto-positron")
        st.plotly_chart(fig_7, use_container_width=True)
        # figs.append(fig_7)
    return figs
