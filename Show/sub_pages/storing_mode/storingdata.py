# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
import pandas as pd
import streamlit as st
import plotly.express as px
from Show.core.GetData import get_all_data


def pool_col(func):
    return func

def st_storingdata(select_data):
    layout_height = 600
    col2, space2, col3 = st.columns((10, 1, 10))
    col4, space4, col5 = st.columns((10, 1, 10))
    stop = st.sidebar.checkbox('Hoog niveau storing')
    if len(select_data) > 0:
        
        all_data_list, wissel_list = get_all_data(select_data, path='storing')
        
        wissel_list.sort()
        # select_wissel = st.sidebar.selectbox('Kies een wissel', wissel_list)
        select_wissel = wissel_list[0]
        # all_data_df = pd.concat(all_data_list)
        all_data_df_list = []
        for i in all_data_list:
            fig_data_df = i.get(select_wissel)[i.get(select_wissel)['storing'] != 'wissel buiten dienst']
            all_data_df_list.append(fig_data_df)
        fig_data_1 = pd.concat(all_data_df_list)
        if stop:
            fig_data = fig_data_1[fig_data_1['wissel stop'] == 1]
        else:
            fig_data = fig_data_1
        st.dataframe(fig_data)
        
        with col2:
            fig_storing_2 = px.pie(fig_data,
                                       values='count',
                                       names='afdelling',
                                       title='Afdelling percentage',
                                       color_discrete_sequence=px.colors.sequential.RdBu,
                                       height=layout_height,
                                       hole=.25,
                                       template='seaborn'
                                      )
            fig_storing_2.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_storing_2, use_container_width=True)
            
        with col3:
            fig_storing_4 = px.pie(fig_data,
                                       values='count',
                                       names='Wissel Nr',
                                       title='Wissel percentage',
                                       color_discrete_sequence=px.colors.sequential.RdBu,
                                       height=layout_height,
                                       hole=.25,
                                       template='seaborn'
                                      )
            fig_storing_4.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_storing_4, use_container_width=True)
            
        with col4:
            fig_storing_3 = px.pie( fig_data,
                                    values='count',
                                    names='storing',
                                    title='Storing percentage',
                                    color_discrete_sequence=px.colors.sequential.RdBu,
                                    height=layout_height,
                                    hole=.25,
                                    template='seaborn', 
                                      )
            fig_storing_3.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_storing_3, use_container_width=True)

        with col5:
            loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
            wagen_loc = pd.merge(loc_df, fig_data, on=['Wissel Nr'], how='inner')
            # st.map(wagen_loc, zoom=10)
            fig_7 = px.scatter_mapbox(wagen_loc, 
                                  lat="latitude", lon="longitude",
                                  color_discrete_sequence=px.colors.sequential.RdBu, 
                                  height=layout_height, size_max=15, zoom=10,color='Wissel Nr',
                                  hover_data=['Wissel Nr'],mapbox_style="carto-positron")
            st.plotly_chart(fig_7)
            
        # def col2_():
        #     with col2:
        #         fig_storing_1 = px.sunburst(fig_data,
        #                                     title='Afdelling overzicht',
        #                                     path=['afdelling', 'storing', 'Wissel Nr', 'wagen nr', 'begin tijd'], 
        #                                     values='count', 
        #                                     color='afdelling',
        #                                     color_continuous_scale=px.colors.sequential.RdBu,
        #                                     hover_data=['begin tijd', 'eind tijd', 'lijn nr', 'categorie', 'service', 'wagen nr'],
        #                                     height=layout_height,
        #                                     template='seaborn')
        #         st.plotly_chart(fig_storing_1, use_container_width=True)
        # def col3_():
        #     with col3:
        #         fig_storing_1 = px.sunburst(fig_data,
        #                                     title='Wissel overzicht',
        #                                     path=['Wissel Nr','wagen nr','afdelling','storing', 'begin tijd'], 
        #                                     values='count', 
        #                                     color='wagen nr',
        #                                     color_continuous_scale=px.colors.sequential.RdBu,
        #                                     hover_data=['begin tijd', 'eind tijd', 'lijn nr', 'categorie', 'service', 'wagen nr'],
        #                                     height=layout_height,
        #                                     template='seaborn')
        #         st.plotly_chart(fig_storing_1, use_container_width=True)
        # def col4_():
        #     with col4:
        #         fig_storing_1 = px.sunburst(fig_data,
        #                                     title='Storing overzicht',
        #                                     path=['storing', 'Wissel Nr', 'afdelling', 'wagen nr', 'begin tijd'], 
        #                                     values='count', 
        #                                     color='storing',
        #                                     color_continuous_scale=px.colors.sequential.RdBu,
        #                                     hover_data=['begin tijd', 'eind tijd', 'lijn nr', 'categorie', 'service', 'wagen nr'],
        #                                     height=layout_height,
        #                                     template='seaborn')
        #         st.plotly_chart(fig_storing_1, use_container_width=True)
        # def col5_():
        #     with col5:
        #         loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
        #         wagen_loc = pd.merge(loc_df, fig_data, on=['Wissel Nr'], how='inner')
        #         # st.map(wagen_loc, zoom=10)
        #         fig_7 = px.scatter_mapbox(wagen_loc, 
        #                               lat="latitude", lon="longitude",
        #                               color_discrete_sequence=px.colors.sequential.RdBu, 
        #                               height=layout_height, size_max=15, zoom=10,color='Wissel Nr',
        #                               hover_data=['Wissel Nr'],mapbox_style="carto-positron")
        #         st.plotly_chart(fig_7)
        # col2_()
        # col3_()
        # col4_()
        # col5_()
        # col_list = [col2_(),col3_(),col4_(),col5_()]
        # with Pool(4) as p:
        #     p.map(pool_col, col_list)

#         p2 = multiprocessing.Process(target=col2_)
#         p3 = multiprocessing.Process(target=col3_)
#         p4 = multiprocessing.Process(target=col4_)
#         p5 = multiprocessing.Process(target=col5_)
#         p2.start()
#         p3.start()
#         p4.start()
#         p5.start()

#         p2.join()
#         p3.join()
#         p4.join()
#         p5.join()
        
        # threads = [threading.Thread(target=col2_),threading.Thread(target=col3_),threading.Thread(target=col4_),threading.Thread(target=col5_)]
        # for t in threads:
        # # 启动线程
        #     t.start()
    else:
        st.title('Kies een gegeven om te analyseren')

