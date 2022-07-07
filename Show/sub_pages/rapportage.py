# ！/usr/bin/python3
# coding:utf-8
# sys


from __init__ import *
import calendar
import datetime
import streamlit as st
from Show.core.GetData import create_download_link
from Show.sub_pages.rapport_mode.snelheid_rep import snelheid_rapport
from fpdf import FPDF
from tempfile import NamedTemporaryFile
import pandas as pd
import plotly.express as px
import plotly.io as pio
# import datapane as dp

def rapportage():
    today = datetime.date.today()
    year, week_nr, day_of_week = today.isocalendar()
    # last_week = week_nr - 1
    mode = st.sidebar.radio(
        'rapport frequentie', ('Wekelijks rapport', 'Maandelijks rapport','Jaarlijks rapport')
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
        
        export_as_pdf = st.sidebar.button("Download Rapport")
        if export_as_pdf:
                pdf = FPDF()
                for fig in w_speed:
                    pdf.add_page(orientation='L')
                    with NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                        pio.write_image(fig, tmpfile.name, height=500)
                        pdf.image(tmpfile.name, 10, 10)
                    
                html = create_download_link(pdf.output(dest="S").encode("latin-1"),f'{mode}-week:{last_week}')
                st.sidebar.markdown(html, unsafe_allow_html=True)
                # pdf.output(dest="F", name=os.path.join(rootPath, f'{mode}-week:{last_week}.pdf'))

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
        
        export_as_pdf = st.sidebar.button("Download Rapport")
        if export_as_pdf:
                pdf = FPDF()
                for fig in m_speed:
                    pdf.add_page(orientation='L')
                    with NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                        pio.write_image(fig, tmpfile.name, height=500)
                        pdf.image(tmpfile.name, 10, 10)
                    
                html = create_download_link(pdf.output(dest="S").encode("latin-1"),f'{mode}-Maand:{last_month}')
                st.sidebar.markdown(html, unsafe_allow_html=True)
        
    elif mode == 'Jaarlijks rapport':
        year = '2022'
        str_year_date = [i[:-3] for i in os.listdir(os.path.join(rootPath, 'DataBase', 'snelheid')) if year in i]
        str_year_date.sort()
        y_speed = snelheid_rapport(str_year_date, 'year')
        export_as_pdf = st.sidebar.button("Download Rapport")
        if export_as_pdf:
                pdf = FPDF()
                for fig in y_speed:
                    pdf.add_page(orientation='L')
                    with NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                        pio.write_image(fig, tmpfile.name, height=500)
                        pdf.image(tmpfile.name, 10, 10)
                    
                html = create_download_link(pdf.output(dest="S").encode("latin-1"),f'{mode}-{year}')
                st.sidebar.markdown(html, unsafe_allow_html=True)
        


