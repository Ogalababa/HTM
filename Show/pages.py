# ！/usr/bin/python3
# coding:utf-8

# os
import pandas as pd
import plotly.express as px
import plotly.io as pio

# streamlit
import streamlit as st
import GetData

from fpdf import FPDF
from tempfile import NamedTemporaryFile


# customize function


def intro():
    st.sidebar.success("Selecteer een pagina hierboven")

    st.markdown(
        """
        ### Dit is een HTM Data-analyse project.

        ##### **👈 Selecteer een pagina in de vervolgkeuzelijst aan de linkerkant** 
        om meer analysetools te zien!
    """
    )


def wissel_gebruiks(select_data):
    col2, space2, col3 = st.columns((10, 1, 10))
    if len(select_data) > 0:
        with col2:
            df_all_data = GetData.get_sql_wissel_nr(select_data)
            wissel_series = df_all_data['wissel nr'].value_counts()
            df_wissel = wissel_series.to_frame()
            df_wissel = df_wissel.rename(columns={'wissel nr': 'Total operated'})
            df_wissel = df_wissel.rename_axis('wissel nr').reset_index()
            fig_wissel = px.bar(df_wissel, title='Total operation', x='wissel nr', y='Total operated',
                                color='Total operated',
                                hover_name='wissel nr',
                                hover_data=['Total operated'],
                                range_color=(0, wissel_series.max()),
                                range_x=(0, 10),
                                color_continuous_scale=px.colors.sequential.Reds)
            st.plotly_chart(fig_wissel, use_container_width=True)

        with col3:
            df_nr_time = GetData.get_sql_wissel_time(select_data)
            df_group = df_nr_time.groupby([pd.Grouper(key='date-time', freq='1min'),
                                           df_nr_time['wissel nr']]).size().reset_index(name='count')
            df_group['time'] = pd.to_datetime(df_group['date-time']).dt.time
            time_fig = px.scatter(df_group, 'date-time', 'count',
                                  title='Wissel pressure/min',
                                  color='wissel nr', labels='Wissel nr',
                                  size='count', hover_name='wissel nr',
                                  hover_data=['time'],
                                  )
            st.plotly_chart(time_fig, use_container_width=True)
    else:
        st.title('Kies een gegevens om te analyseren')


def tram_speed(select_data):
    layout_height = 600
    figs = []

    if len(select_data) > 0:
        df_all_data = GetData.get_tram_speed(select_data)
        mode = st.sidebar.radio(
            'Grafiek mode：',
            ('Max waarde', 'Grafiek per wissel', 'Grafiek per wagen')
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

            wissel_list = list(set(df_all_data['Wissel Nr']))
            wissel_list.sort()
            selected_wissel = st.sidebar.selectbox('Kies een wissel', wissel_list)
            df_all_data = df_all_data.set_index('Wissel Nr', drop=False, )

            with col2:
                fig_wissel_4 = px.bar(df_all_data.loc[selected_wissel].sort_values(by='snelheid km/h'),
                                      title='Wagen/snelheid overzicht',
                                      x='Wagen Nr', y='snelheid km/h',
                                      color='snelheid km/h',
                                      height=layout_height,
                                      hover_data=['Lijn',
                                                  'Wagen Nr',
                                                  'Categorie',
                                                  'Service',
                                                  'Tijd'],
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
                                                      'Service'],
                                          color='Wagen Nr',
                                          color_continuous_scale=px.colors.sequential.Sunsetdark,
                                          size='snelheid km/h',
                                          height=layout_height,
                                          )
                st.plotly_chart(fig_wissel_1, use_container_width=True)
                figs.append(fig_wissel_1)

            with col4:
                speed_counts_wissel = df_all_data.loc[selected_wissel].copy()
                speed_counts_wissel['hoeveelheid'] = 1
                speed_counts_wissel['Tijd'] = speed_counts_wissel['Tijd'].astype(str)
                fig_counts = px.sunburst(speed_counts_wissel,
                                         title='Snelheid overzicht',
                                         path=['Wissel Nr', 'snelheid km/h', 'Wagen Nr', 'Tijd'],
                                         values='hoeveelheid',
                                         color='snelheid km/h',
                                         color_continuous_scale=px.colors.sequential.RdBu,
                                         height=layout_height,
                                         hover_data=[
                                             'Categorie',
                                             'Service',
                                             'Tijd'
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
                fig_wissel_2.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_wissel_2, use_container_width=True)
                figs.append(fig_wissel_2)

        else:
            col2, space2, col3 = st.columns((10, 1, 10))
            col4, space4, col5 = st.columns((10, 1, 10))
            wagen_list = list(set(df_all_data['Wagen Nr']))
            wagen_list.sort()
            selected_wagen = st.sidebar.selectbox('Kies een wagen', wagen_list)
            df_all_data = df_all_data.set_index('Wagen Nr', drop=False)

            with col2:
                fig_wagen_2 = px.bar(df_all_data.loc[selected_wagen].sort_values(by='snelheid km/h'),
                                     title='Wissel/snelheid overzicht',
                                     x='Wissel Nr', y='snelheid km/h',
                                     color='snelheid km/h',
                                     height=layout_height,
                                     hover_data=['Lijn',
                                                 'Wissel Nr',
                                                 'Categorie',
                                                 'Service',
                                                 'Tijd'],
                                     color_continuous_scale=px.colors.sequential.Sunsetdark)
                st.plotly_chart(fig_wagen_2, use_container_width=True)
                figs.append(fig_wagen_2)

            with col3:
                fig_wagen = px.scatter(df_all_data.loc[selected_wagen],
                                       x='Tijd', y='snelheid km/h',
                                       title='Wissel snelheid/tijd grafiek',
                                       hover_data=['Lijn',
                                                   'Wissel Nr',
                                                   'Categorie',
                                                   'Service'],
                                       color='Wissel Nr',
                                       color_continuous_scale=px.colors.sequential.Sunsetdark,
                                       size='snelheid km/h',
                                       height=layout_height,
                                       )
                st.plotly_chart(fig_wagen, use_container_width=True)
                figs.append(fig_wagen)

            with col4:
                speed_counts = df_all_data.loc[selected_wagen].copy()
                speed_counts['hoeveelheid'] = 1
                speed_counts['Tijd'] = speed_counts['Tijd'].astype(str)
                fig_counts_2 = px.sunburst(speed_counts,
                                           title='Snelheid overzicht',
                                           path=['Wagen Nr', 'snelheid km/h', 'Wissel Nr', 'Tijd'],
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
                fig_wissel_3.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_wissel_3, use_container_width=True)
                figs.append(fig_wissel_3)

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
                html = GetData.create_download_link(pdf.output(dest="S").encode("latin-1"),
                                                    f'{mode}_{select_data[-1]}_{select_data[0]}')
            else:
                html = GetData.create_download_link(pdf.output(dest="S").encode("latin-1"),
                                                    f'{mode}-{select_data[0]}')
            st.sidebar.markdown(html, unsafe_allow_html=True)
        if export_as_csv:
            csv = df_all_data[[
                'Lijn', 'Wagen Nr', 'Categorie',
                'Service', 'Wissel Nr', 'Tijd',
                'snelheid km/h']].to_csv().encode()
            if len(select_data) >= 2:
                href = GetData.create_download_link(csv, f'{select_data[-1]}_{select_data[0]}', 'csv')
            else:
                href = GetData.create_download_link(csv, select_data[0], 'csv')
            st.sidebar.markdown(href, unsafe_allow_html=True)

    else:
        st.title('Kies een gegeven om te analyseren')
