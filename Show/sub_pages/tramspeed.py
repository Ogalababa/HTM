# ！/usr/bin/python3
# coding:utf-8
# sys
from Show.core import GetData
from __init__ import *
import pandas as pd
import plotly.express as px
import plotly.io as pio

# streamlit
import streamlit as st
from Show.core.GetData import get_tram_speed, create_download_link, get_data_name
from fpdf import FPDF
from tempfile import NamedTemporaryFile


def tram_speed():
    # get database file name
    # 获取数据库文件名
    try:
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
                'Snelheidswaarschuwing', 'Max waarde', 'Grafiek per wissel', 'Grafiek per wagen', 'Grafiek per lijn')
            )
            if mode == 'Max waarde':
                col2, space2, col3 = st.columns((10, 1, 10))
                col4, space4, col5 = st.columns((10, 1, 10))

                with col2:
                    wissel_base = df_all_data.set_index('Wissel Nr', drop=False, inplace=False).sort_index()
                    fig_max_wissel = px.bar(wissel_base.groupby(
                        pd.Grouper(key='Wissel Nr')).max().rename_axis(
                        'Wissel Nr').reset_index().sort_values(by='snelheid km/h'),
                                            title='Max snelheid per wissel',
                                            x='Wissel Nr', y='snelheid km/h',
                                            color='snelheid km/h',
                                            color_continuous_scale=px.colors.sequential.Reds)
                    st.plotly_chart(fig_max_wissel, use_container_width=True)
                    figs.append(fig_max_wissel)

                with col3:
                    wagen_base = df_all_data.set_index('Wagen Nr', drop=False, inplace=False).sort_index()
                    fig_max_wagen = px.bar(wagen_base.groupby(
                        pd.Grouper(key='Wagen Nr')).max().rename_axis(
                        'Wagen Nr').reset_index().sort_values(by='snelheid km/h'),
                                           title='Max snelheid per wagen',
                                           x='Wagen Nr', y='snelheid km/h',
                                           color='snelheid km/h',
                                           color_continuous_scale=px.colors.sequential.Blues)
                    st.plotly_chart(fig_max_wagen, use_container_width=True)
                    figs.append(fig_max_wagen)

                with col4:
                    wissel_base = df_all_data.set_index('Wissel Nr', drop=False, inplace=False).sort_index()
                    fig_mean_wissel = px.bar(wissel_base.groupby(
                        pd.Grouper(key='Wissel Nr')).mean().round(0).rename_axis(
                        'Wissel Nr').reset_index().sort_values(by='snelheid km/h'),
                                             title='Gemiddeld snelheid per wissel',
                                             x='Wissel Nr', y='snelheid km/h',
                                             color='snelheid km/h',
                                             color_continuous_scale=px.colors.sequential.Burg)
                    st.plotly_chart(fig_mean_wissel, use_container_width=True)
                    figs.append(fig_mean_wissel)

                with col5:
                    wagen_base = df_all_data.set_index('Wagen Nr', drop=False, inplace=False).sort_index()
                    fig_mean_wagen = px.bar(wagen_base.groupby(
                        pd.Grouper(key='Wagen Nr')).mean().round(0).rename_axis(
                        'Wagen Nr').reset_index().sort_values(by='snelheid km/h'),
                                            title='Gemiddeld snelheid per wagen',
                                            x='Wagen Nr', y='snelheid km/h',
                                            color='snelheid km/h',
                                            color_continuous_scale=px.colors.sequential.dense)
                    st.plotly_chart(fig_mean_wagen, use_container_width=True)
                    figs.append(fig_mean_wagen)

            elif mode == 'Grafiek per wissel':
                col2, space2, col3 = st.columns((10, 1, 10))
                col4, space4, col5 = st.columns((10, 1, 10))
                col6, space6, col7 = st.columns((10, 1, 10))

                wissel_list = list(set(df_all_data['Wissel Nr']))
                wissel_list.sort()
                selected_wissel = st.sidebar.selectbox('Kies een wissel', wissel_list)
                df_all_data = df_all_data.set_index('Wissel Nr', drop=False, )
                speed_counts_wissel = df_all_data.loc[selected_wissel].copy()
                speed_counts_wissel['hoeveelheid'] = 1
                with col2:
                    fig_wissel_4 = px.bar(speed_counts_wissel.sort_values(by='snelheid km/h'),
                                          title='Wagen/snelheid overzicht',
                                          x='snelheid km/h', y='hoeveelheid',
                                          color='code',
                                          height=layout_height,
                                          hover_data=['Lijn',
                                                      'Wagen Nr',
                                                      'Categorie',
                                                      'Service',
                                                      'Tijd',
                                                      'Richting'],
                                          color_continuous_scale=px.colors.sequential.Sunsetdark)
                    st.plotly_chart(fig_wissel_4, use_container_width=True)
                    figs.append(fig_wissel_4)

                with col3:
                    fig_wissel_1 = px.scatter(df_all_data.loc[selected_wissel],
                                              x='Tijd', y='snelheid km/h',
                                              title='Snelheid/tijd overzicht',
                                              hover_data=['Lijn',
                                                          'Wagen Nr',
                                                          'Categorie',
                                                          'Service',
                                                          'Richting'],
                                              color='code',
                                              color_continuous_scale=px.colors.sequential.Sunsetdark,
                                              size='snelheid km/h',
                                              symbol='Richting',
                                              height=layout_height,
                                              )
                    st.plotly_chart(fig_wissel_1, use_container_width=True)
                    figs.append(fig_wissel_1)

                with col4:
                    speed_counts_wissel['Tijd'] = speed_counts_wissel['Tijd'].astype(str)
                    fig_counts = px.sunburst(speed_counts_wissel,
                                             title='Snelheid overzicht',
                                             path=['snelheid km/h', 'Richting', 'code'],
                                             values='hoeveelheid',
                                             color='snelheid km/h',
                                             color_continuous_scale=px.colors.sequential.RdBu,
                                             height=layout_height,
                                             hover_data=[
                                                 'Categorie',
                                                 'Service',
                                                 'Richting'
                                             ])
                    st.plotly_chart(fig_counts, use_container_width=True)
                    figs.append(fig_counts)

                with col5:
                    fig_wissel_2 = px.pie(speed_counts_wissel,
                                          values='hoeveelheid',
                                          names='snelheid km/h',
                                          title='Snelheid percentage',
                                          color_discrete_sequence=px.colors.sequential.RdBu,
                                          height=layout_height,
                                          hole=.25,
                                          )
                    # fig_wissel_2.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig_wissel_2, use_container_width=True)
                    figs.append(fig_wissel_2)

                with col6:
                    fig_wissel_4 = px.pie(speed_counts_wissel,
                                          values='hoeveelheid',
                                          names='Richting',
                                          title='Richting percentage',
                                          color_discrete_sequence=px.colors.sequential.RdBu,
                                          height=layout_height,
                                          hole=.25,
                                          )
                    # fig_wissel_4.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig_wissel_4, use_container_width=True)
                    figs.append(fig_wissel_4)
                with col7:
                    loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
                    # st.map(loc_df[loc_df['Wissel Nr'] == selected_wissel], zoom=10)
                    fig_7 = px.scatter_mapbox(loc_df[loc_df['Wissel Nr'] == selected_wissel], 
                                          lat="latitude", lon="longitude",
                                          color_discrete_sequence=px.colors.sequential.RdBu, 
                                          height=layout_height, size_max=15, zoom=13,color='Wissel Nr',
                                          hover_data=['Wissel Nr'],mapbox_style="carto-positron")
                    st.plotly_chart(fig_7)
                    figs.append(fig_7)

            elif mode == 'Grafiek per wagen':
                col2, space2, col3 = st.columns((10, 1, 10))
                col4, space4, col5 = st.columns((10, 1, 10))
                col6, space6, col7 = st.columns((10, 1, 10))
                wagen_list = list(set(df_all_data['Wagen Nr']))
                ex_list = list(map(str, range(1000)))
                # wagen_list = [i for i in wagen_list if i != '0']
                wagen_list = [i for i in wagen_list if i not in ex_list]
                wagen_list.sort()
                selected_wagen = st.sidebar.selectbox('Kies een wagen', wagen_list)
                df_all_data = df_all_data.set_index('Wagen Nr', drop=False)
                speed_counts = df_all_data.loc[selected_wagen].copy()
                speed_counts['hoeveelheid'] = 1

                with col2:
                    try:
                        fig_wagen_2 = px.bar(speed_counts.sort_values(by='snelheid km/h'),
                                             title='Wissel/snelheid overzicht',
                                             x='snelheid km/h', y='hoeveelheid',
                                             color='code',
                                             height=layout_height,
                                             hover_data=['Lijn',
                                                         'Wissel Nr',
                                                         'Categorie',
                                                         'Service',
                                                         'Tijd',
                                                         'Richting'],
                                             color_continuous_scale=px.colors.sequential.Sunsetdark)
                        st.plotly_chart(fig_wagen_2, use_container_width=True)
                        figs.append(fig_wagen_2)
                    except:
                        st.title('Geen Data')

                with col3:
                    fig_wagen = px.scatter(df_all_data.loc[selected_wagen],
                                           x='Tijd', y='snelheid km/h',
                                           title='Wissel snelheid/tijd grafiek',
                                           hover_data=['Lijn',
                                                       'Wissel Nr',
                                                       'Categorie',
                                                       'Service',
                                                       'Richting'],
                                           color='code',
                                           color_continuous_scale=px.colors.sequential.Sunsetdark,
                                           size='snelheid km/h',
                                           symbol='Richting',
                                           height=layout_height,
                                           )
                    st.plotly_chart(fig_wagen, use_container_width=True)
                    figs.append(fig_wagen)

                with col4:
                    speed_counts['Tijd'] = speed_counts['Tijd'].astype(str)
                    fig_counts_2 = px.sunburst(speed_counts,
                                               title='Snelheid overzicht',
                                               path=['code', 'snelheid km/h', 'Richting', 'Wissel Nr'],
                                               values='hoeveelheid',
                                               color='snelheid km/h',
                                               color_continuous_scale=px.colors.sequential.RdBu,
                                               height=layout_height,
                                               hover_data=[
                                                   'Categorie',
                                                   'Service',
                                               ])
                    st.plotly_chart(fig_counts_2, use_container_width=True)
                    figs.append(fig_counts_2)

                with col5:
                    fig_wissel_3 = px.pie(speed_counts,
                                          values='hoeveelheid',
                                          names='snelheid km/h',
                                          title='Snelheid percentage',
                                          color_discrete_sequence=px.colors.sequential.RdBu,
                                          height=layout_height,
                                          hole=.25,
                                          )
                    # fig_wissel_3.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig_wissel_3, use_container_width=True)
                    figs.append(fig_wissel_3)

                with col6:
                    fig_wissel_5 = px.pie(speed_counts,
                                          values='hoeveelheid',
                                          names='Richting',
                                          title='Richting percentage',
                                          color_discrete_sequence=px.colors.sequential.RdBu,
                                          height=layout_height,
                                          hole=.25,
                                          )
                    # fig_wissel_5.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig_wissel_5, use_container_width=True)
                    figs.append(fig_wissel_5)

                with col7:
                    loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
                    wagen_loc = pd.merge(loc_df, speed_counts, on=['Wissel Nr'], how='inner')
                    # st.map(wagen_loc, zoom=10)
                    fig_7 = px.scatter_mapbox(wagen_loc, 
                                          lat="latitude", lon="longitude",
                                          color_discrete_sequence=px.colors.sequential.RdBu, 
                                          height=layout_height, size_max=15, zoom=10,color='Wissel Nr',
                                          hover_data=['Wissel Nr'],mapbox_style="carto-positron")
                    st.plotly_chart(fig_7)
                    figs.append(fig_7)

            elif mode == 'Snelheidswaarschuwing':
                
                col1, space1, col1_1 = st.columns((21, 0.1, 0.1))
                col2, space2, col3 = st.columns((10, 1, 10))
                col4, space4, col5 = st.columns((10, 1, 10))
                col6, space6, col7 = st.columns((10, 1, 10))
                max_snelheid = max(df_all_data['snelheid km/h'].tolist())
                if max_snelheid >= 25:
                    select_speed = st.sidebar.number_input('Vul de waarschuwing snelheid in (km/h)', min_value=15,
                                                           max_value=max(df_all_data['snelheid km/h'].tolist()),
                                                           step=1, value=25)
                else:
                    select_speed = st.sidebar.number_input('Vul de waarschuwing snelheid in (km/h)',
                                                           min_value=15,
                                                           max_value=max_snelheid,
                                                           step=1, value=(max_snelheid - 2))
                df_all_data = df_all_data[df_all_data['snelheid km/h'] >= select_speed]
                # wagen_list = list(set(df_all_data['Lijn']))
                # wagen_list = [i for i in wagen_list if i != 0]
                # wagen_list.sort()
                # selected_lijn = st.sidebar.selectbox('Kies een lijn nr', wagen_list)
                # df_all_data = df_all_data.set_index('Lijn', drop=False)
                speed_counts = df_all_data.copy()
                speed_counts['hoeveelheid'] = 1
                richting = st.sidebar.radio("kiss een richting", ('alles', 'recht door', 'rechts/links af'))
                if richting == 'rechts/links af':
                    speed_counts = speed_counts[(speed_counts['Richting'] == ' rechts af') | (speed_counts['Richting'] == ' links af')]
                elif richting == 'recht door':
                    speed_counts = speed_counts[speed_counts['Richting'] == 'Recht door']
                else:
                    pass
                
                with col1:
                    st.sidebar.metric(f'Totale records boven {select_speed} km/h:', len(speed_counts), delta=f'{round(((len(speed_counts)/speed_record_size)*100),3)}% van totale records',
                                      delta_color="normal")

                with col2:
                    fig_wagen_2 = px.bar(speed_counts.sort_values(by='snelheid km/h'),
                                         title='Wissel/snelheid overzicht',
                                         x='snelheid km/h', y='hoeveelheid',
                                         color='code',
                                         height=layout_height,
                                         hover_data=['Lijn',
                                                     'Wissel Nr',
                                                     'Categorie',
                                                     'Service',
                                                     'Tijd',
                                                     'Richting'],
                                         color_continuous_scale=px.colors.sequential.Sunsetdark)
                    st.plotly_chart(fig_wagen_2, use_container_width=True)
                    figs.append(fig_wagen_2)

                with col3:
                    fig_wagen = px.scatter(speed_counts,
                                           x='Tijd', y='snelheid km/h',
                                           title='Wissel snelheid/tijd grafiek',
                                           hover_data=['Lijn',
                                                       'Wissel Nr',
                                                       'Categorie',
                                                       'Service',
                                                       'Richting'],
                                           color='code',
                                           color_continuous_scale=px.colors.sequential.Sunsetdark,
                                           size='snelheid km/h',
                                           symbol='Richting',
                                           height=layout_height,
                                           )
                    st.plotly_chart(fig_wagen, use_container_width=True)
                    figs.append(fig_wagen)

                with col4:
                    speed_counts['Tijd'] = speed_counts['Tijd'].astype(str)
                    fig_counts_2 = px.sunburst(speed_counts,
                                               title='Snelheid overzicht',
                                               path=['snelheid km/h', 'code'],
                                               values='hoeveelheid',
                                               color='snelheid km/h',
                                               color_continuous_scale=px.colors.sequential.RdBu,
                                               height=layout_height,
                                               hover_data=[
                                                   'Categorie',
                                                   'Service',
                                               ])
                    st.plotly_chart(fig_counts_2, use_container_width=True)
                    figs.append(fig_counts_2)

                with col5:
                    fig_wissel_3 = px.pie(speed_counts,
                                          values='hoeveelheid',
                                          names='snelheid km/h',
                                          title='Snelheid percentage',
                                          color_discrete_sequence=px.colors.sequential.RdBu,
                                          height=layout_height,
                                          hole=.25,
                                          )
                    fig_wissel_3.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig_wissel_3, use_container_width=True)
                    figs.append(fig_wissel_3)

                with col6:
                    fig_wissel_5 = px.pie(speed_counts,
                                          values='hoeveelheid',
                                          names='Richting',
                                          title='Richting percentage',
                                          color_discrete_sequence=px.colors.sequential.RdBu,
                                          height=layout_height,
                                          hole=.25,
                                          )
                    fig_wissel_5.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig_wissel_5, use_container_width=True)
                    figs.append(fig_wissel_5)

                with col7:
                    loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
                    wagen_loc = pd.merge(loc_df, speed_counts, on=['Wissel Nr'], how='inner')
                    # st.map(wagen_loc, zoom=10)
                    fig_7 = px.scatter_mapbox(wagen_loc, 
                                          lat="latitude", lon="longitude",
                                          color_discrete_sequence=px.colors.sequential.RdBu, 
                                          height=layout_height, size_max=15, zoom=10,color='Wissel Nr',
                                          hover_data=['Wissel Nr'],mapbox_style="carto-positron")
                    st.plotly_chart(fig_7)
                    figs.append(fig_7)

            else:
                col2, space2, col3 = st.columns((10, 1, 10))
                col4, space4, col5 = st.columns((10, 1, 10))
                col6, space6, col7 = st.columns((10, 1, 10))
                wagen_list = list(set(df_all_data['Lijn']))
                wagen_list = [i for i in wagen_list if i != 0]
                wagen_list.sort()
                selected_lijn = st.sidebar.selectbox('Kies een lijn nr', wagen_list)
                df_all_data = df_all_data.set_index('Lijn', drop=False)
                speed_counts = df_all_data.loc[selected_lijn].copy()
                speed_counts['hoeveelheid'] = 1
                with col2:
                    fig_wagen_2 = px.bar(speed_counts.sort_values(by='snelheid km/h'),
                                         title='Wissel/snelheid overzicht',
                                         x='snelheid km/h', y='hoeveelheid',
                                         color='code',
                                         height=layout_height,
                                         hover_data=['Lijn',
                                                     'Wissel Nr',
                                                     'Categorie',
                                                     'Service',
                                                     'Tijd',
                                                     'Richting'],
                                         color_continuous_scale=px.colors.sequential.Sunsetdark)
                    st.plotly_chart(fig_wagen_2, use_container_width=True)
                    figs.append(fig_wagen_2)

                with col3:
                    fig_wagen = px.scatter(df_all_data.loc[selected_lijn],
                                           x='Tijd', y='snelheid km/h',
                                           title='Wissel snelheid/tijd grafiek',
                                           hover_data=['Lijn',
                                                       'Wissel Nr',
                                                       'Categorie',
                                                       'Service',
                                                       'Richting'],
                                           color='code',
                                           color_continuous_scale=px.colors.sequential.Sunsetdark,
                                           size='snelheid km/h',
                                           height=layout_height,
                                           )
                    st.plotly_chart(fig_wagen, use_container_width=True)
                    figs.append(fig_wagen)

                with col4:
                    speed_counts['Tijd'] = speed_counts['Tijd'].astype(str)
                    fig_counts_2 = px.sunburst(speed_counts,
                                               title='Snelheid overzicht',
                                               path=['snelheid km/h','code'],
                                               values='hoeveelheid',
                                               color='snelheid km/h',
                                               color_continuous_scale=px.colors.sequential.RdBu,
                                               height=layout_height,
                                               hover_data=[
                                                   'Categorie',
                                                   'Service',
                                                   'Tijd'
                                               ])
                    st.plotly_chart(fig_counts_2, use_container_width=True)
                    figs.append(fig_counts_2)

                with col5:
                    fig_wissel_3 = px.pie(speed_counts,
                                          values='hoeveelheid',
                                          names='snelheid km/h',
                                          title='Snelheid percentage',
                                          color_discrete_sequence=px.colors.sequential.RdBu,
                                          height=layout_height,
                                          hole=.25,
                                          )
                    # fig_wissel_3.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig_wissel_3, use_container_width=True)
                    figs.append(fig_wissel_3)

                with col6:
                    fig_wissel_5 = px.pie(speed_counts,
                                          values='hoeveelheid',
                                          names='Richting',
                                          title='Richting percentage',
                                          color_discrete_sequence=px.colors.sequential.RdBu,
                                          height=layout_height,
                                          hole=.25,
                                          )
                    # fig_wissel_5.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig_wissel_5, use_container_width=True)
                    figs.append(fig_wissel_5)

                with col7:
                    loc_df = pd.read_csv(os.path.join(rootPath, 'DataBase', 'norm', 'gps_info.csv'), sep=';')
                    wagen_loc = pd.merge(loc_df, speed_counts, on=['Wissel Nr'], how='inner')
                    # st.map(wagen_loc, zoom=10)
                    fig_7 = px.scatter_mapbox(wagen_loc, 
                                          lat="latitude", lon="longitude",
                                          color_discrete_sequence=px.colors.sequential.RdBu, 
                                          height=layout_height, size_max=15, zoom=10,color='Wissel Nr',
                                          hover_data=['Wissel Nr'],mapbox_style="carto-positron")
                    st.plotly_chart(fig_7)
                    figs.append(fig_7)

            export_as_pdf = st.sidebar.button("Download Rapport")
            export_as_csv = st.sidebar.button("Download Details")
            if export_as_pdf:
                pdf = FPDF()
                for fig in figs:
                    pdf.add_page(orientation='L')
                    with NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                        pio.write_image(fig, tmpfile.name, height=500)
                        pdf.image(tmpfile.name, 10, 10)
                if len(select_data) >= 2:
                    html = create_download_link(pdf.output(dest="S").encode("latin-1"),
                                                f'{mode}_{select_data[-1]}_{select_data[0]}')
                else:
                    html = create_download_link(pdf.output(dest="S").encode("latin-1"),
                                                f'{mode}-{select_data[0]}')
                st.sidebar.markdown(html, unsafe_allow_html=True)
            if export_as_csv:
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
    except:
        st.title('Geen data beschikbaar')