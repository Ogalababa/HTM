# ！/usr/bin/python3
# coding:utf-8

# os
from sub_pages.intro import intro
from sub_pages.tramspeed import tram_speed

# def wissel_gebruiks(select_data):
#     col2, space2, col3 = st.columns((10, 1, 10))
#     if len(select_data) > 0:
#         with col2:
#             df_all_data = GetData.get_sql_wissel_nr(select_data)
#             wissel_series = df_all_data['wissel nr'].value_counts()
#             df_wissel = wissel_series.to_frame()
#             df_wissel = df_wissel.rename(columns={'wissel nr': 'Total operated'})
#             df_wissel = df_wissel.rename_axis('wissel nr').reset_index()
#             fig_wissel = px.bar(df_wissel, title='Total operation', x='wissel nr', y='Total operated',
#                                 color='Total operated',
#                                 hover_name='wissel nr',
#                                 hover_data=['Total operated'],
#                                 range_color=(0, wissel_series.max()),
#                                 range_x=(0, 10),
#                                 color_continuous_scale=px.colors.sequential.Reds)
#             st.plotly_chart(fig_wissel, use_container_width=True)
#
#         with col3:
#             df_nr_time = GetData.get_sql_wissel_time(select_data)
#             df_group = df_nr_time.groupby([pd.Grouper(key='date-time', freq='1min'),
#                                            df_nr_time['wissel nr']]).size().reset_index(name='count')
#             df_group['time'] = pd.to_datetime(df_group['date-time']).dt.time
#             time_fig = px.scatter(df_group, 'date-time', 'count',
#                                   title='Wissel pressure/min',
#                                   color='wissel nr', labels='Wissel nr',
#                                   size='count', hover_name='wissel nr',
#                                   hover_data=['time'],
#                                   )
#             st.plotly_chart(time_fig, use_container_width=True)
#     else:
#         st.title('Kies een gegevens om te analyseren')


