# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import pandas as pd
import plotly.express as px

# streamlit
import streamlit as st
from datetime import timedelta

# 
from Show.core.GetData import st_get_alldata_from_db
from Show.core.GetData import st_get_alldata_from_db_cash
from Run.core.Integration.DataInitialization import save_to_sql


def fig_rit(layout_height):
    speed_data = None
    uploaded_file = st.sidebar.file_uploader("Upload een excel bestaand", type='xlsx')
    if uploaded_file is not None:
        rit_data = pd.read_excel(uploaded_file)
        try:
            # 查看是否已处理数据
            rit_db_list = [i[:-3] for i in os.listdir(os.path.join(rootPath, 'DataBase', 'rit')) if '.db' in i]
            # rit数据预处理
            if str((rit_data['datum'][0]).date()) not in rit_db_list:
                # 处理上传的excel文件
                rit_data['time'] = rit_data['datum'].astype('str') + ' ' + rit_data['time'].astype('str')
                rit_data = rit_data.drop(columns=['naam', 'richting', 'haltenr.', 'haltenaam', 'punc'], axis=1)
                rit_data = rit_data.dropna(how='any')
                rit_data = rit_data.astype(
                    {'volgnummer': 'int32', 'voertuig': 'int32', 'ritnummer': 'int32', 'lijn': 'int32'})
                rit_data['time'] = pd.to_datetime(rit_data.time, format='%Y-%m-%d %H:%M:%S')
                rit_list = list(set(rit_data.ritnummer.to_list()))
                date_dict = {'today': str((rit_data['datum'][0]).date()),
                             'yesterday': str((rit_data['datum'][0] - timedelta(days=1)).date())}
                # 匹配数据库
                speed_data_1 = pd.concat(list(st_get_alldata_from_db(date_dict.get('today'), path='snelheid').values()))
                speed_data_2 = pd.concat(list(st_get_alldata_from_db(date_dict.get('yesterday'), path='snelheid').values()))
                speed_data = pd.concat([speed_data_1, speed_data_2])

                # 匹配ritnummer到数据库
                for i in rit_list:
                    rit_nummer = i
                    single_rit = rit_data[rit_data['ritnummer'] == rit_nummer]
                    voertuig_nummer = single_rit.iloc[[0]].voertuig.tolist()[0]
                    rit_start = single_rit[single_rit['volgnummer'] == single_rit['volgnummer'].min()]['time'].tolist()[0]
                    rit_end = single_rit[single_rit['volgnummer'] == single_rit['volgnummer'].max()]['time'].tolist()[0]

                    speed_data.loc[
                        (speed_data['<afmelden> voertuig'] == voertuig_nummer) & (speed_data['hfk_in'] >= rit_start) & (
                                    speed_data['hfk_in'] <= rit_end), 'ritnummer'] = rit_nummer
                speed_data = speed_data.dropna()
                speed_data['hoeveelheid'] = 1
                speed_data = speed_data.rename(columns={'hfk_in': 'Tijd', 'wissel nr': 'Wissel Nr'})
                save_to_sql(date_dict.get('today'), {'all data': speed_data}, path='rit')
            else:
                speed_data = st_get_alldata_from_db_cash(str((rit_data['datum'][0]).date()), path='rit').get('all data')

            # website contain
            # 数据可视化
            col2, space2, col3 = st.columns((10, 1, 10))
            col4, space4, col5 = st.columns((10, 1, 10))
            col6, space6, col7 = st.columns((10, 1, 10))
            # speed_data = speed_data.set_index('ritnummer', drop=False)
            speed_data = speed_data.astype({'ritnummer': 'int32'})
            db_rit_list = list(set(speed_data['ritnummer']))
            db_rit_list.sort()
            selected_rit_nr = st.sidebar.selectbox('Kies een ritnummer', db_rit_list)
            selected_rit = speed_data[speed_data['ritnummer'] == selected_rit_nr]

            with col2:
                fig_rit_2 = px.bar(selected_rit.sort_values(by='snelheid km/h'),
                                   title=f'Snelheid overzicht van rit {selected_rit_nr}',
                                   x='snelheid km/h', y='hoeveelheid', 
                                   color='snelheid km/h', 
                                   height=layout_height, 
                                   hover_data=['Wissel Nr',
                                               'Tijd',
                                               '<afmelden> voertuig',
                                               'Richting'],
                                   color_continuous_scale=px.colors.sequential.Sunsetdark)
                st.plotly_chart(fig_rit_2, use_container_width=True)

            with col3:
                fig_rit_3 = px.scatter(selected_rit,
                                       x='Tijd', y='snelheid km/h',
                                       title='Wissel snelheid/tijd grafiek',
                                       hover_data=[
                                                   'Wissel Nr',
                                                   '<afmelden> voertuig',
                                                   'Richting'],
                                       color='Richting',
                                       color_continuous_scale=px.colors.sequential.Sunsetdark,
                                       size='snelheid km/h',
                                       symbol='Richting',
                                       height=layout_height,
                                       )
                st.plotly_chart(fig_rit_3, use_container_width=True)

            with col4:
                fig_rit_4 = px.pie(selected_rit,
                                      values='hoeveelheid',
                                      names='snelheid km/h',
                                      title='Snelheid percentage',
                                      color_discrete_sequence=px.colors.sequential.RdBu,
                                      height=layout_height,
                                      hole=.25,
                                      )
                # fig_wissel_3.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_rit_4, use_container_width=True)

            with col5:
                loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
                voertuig_loc = pd.merge(loc_df, selected_rit, on=['Wissel Nr'], how='inner')
                # st.map(voertuig_loc, zoom=10)
                fig_7 = px.scatter_mapbox(voertuig_loc,
                                          lat="latitude", lon="longitude",
                                          color_discrete_sequence=px.colors.sequential.RdBu,
                                          height=layout_height, size_max=15, zoom=10, color='Wissel Nr',
                                          hover_data=['Wissel Nr', 'Tijd'], mapbox_style="carto-positron")
                st.plotly_chart(fig_7)
        except KeyError:
            st.error('Ongeldig bestand')
            st.error('Upload een excel bestand met onderstaande formaat!')
            st.dataframe(pd.DataFrame({'naam':['Abcde'], 'datum':['01-01-2022'], 
                                       'volgnummer':['1'], 'time':['01:02:03'], 
                                       'richting':['1234'], 'voertuig':['3045'],
                                       'ritnummer':['123456'], 'lijn':['1'], 'haltenr.':['1234'],
                                       'haltenaam':['abcd'], 'punc':['11']}))

    else:
        st.success('Upload een rit excel bestand om verder te gaan')
        st.warning('Het proces duur maximaal 3 minuten')
    return speed_data
