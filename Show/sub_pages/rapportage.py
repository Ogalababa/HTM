# ！/usr/bin/python3
# coding:utf-8
# sys
import os

from __init__ import *
import streamlit as st
import datetime, calendar
from Show.core.GetData import get_tram_speed, create_download_link, get_data_name
from Show.sub_pages.rapport_mode.snelheid_rep import snelheid_rapport


def rapportage():
    today = datetime.date.today()
    year, week_nr, day_of_week = today.isocalendar()
    # last_week = week_nr - 1
    mode = st.sidebar.radio(
        'rapport frequentie', ('Wekelijks rapport', 'Maandelijks rapport', 'Jaarlijks rapport')
    )
    if mode == 'Wekelijks rapport':
        if week_nr > 1:
            last_week = week_nr - 1
        else:
            last_week = 52
            year = year - 1
        date_of_week = [datetime.date.fromisocalendar(year, last_week, x) for x in range(1, 8)]
        str_week_date = []
        for i in date_of_week:
            str_week_date.append(i.strftime('%Y-%m-%d'))
        w_speed = snelheid_rapport(str_week_date, 'week')

    elif mode == 'Maandelijks rapport':
        last_month = today.month - 1
        if today.month > 1:
            last_month = today.month - 1
        else:
            last_month = 12
            year = year - 1
        cal = calendar.Calendar()
        date_of_month = [x for x in cal.itermonthdates(year, last_month)]
        str_month_date = []
        for i in date_of_month:
            str_month_date.append(i.strftime('%Y-%m-%d'))
        m_speed = snelheid_rapport(str_month_date, 'month')

    elif mode == 'Jaarlijks rapport':
        year = '2022'
        str_year_date = [i[:-3] for i in os.listdir(os.path.join(rootPath, 'DataBase', 'snelheid')) if year in i]
        y_speed = snelheid_rapport(str_year_date, 'year')

