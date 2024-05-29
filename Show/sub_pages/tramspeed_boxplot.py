# ！/usr/bin/python3
# coding:utf-8
# sys
from Show.sub_pages.Utils import generate_dates_within_last_month
from __init__ import *
import calendar
import datetime
import streamlit as st
from Show.core.GetData import create_download_link
from Show.sub_pages.rapport_mode.snelheid_rep import snelheid_rapport
from Show.sub_pages.rapport_mode.storing_rep import storing_rapport
from fpdf import FPDF
from tempfile import NamedTemporaryFile
import pandas as pd
import plotly.express as px
import plotly.io as pio


def speed_boxplot():
    today = datetime.date.today()
    year, week_nr, day_of_week = today.isocalendar()
    mode = st.sidebar.radio(
        "Periode", ("1 maand", '3 maanden', "6 maanden", "12 maanden")
    )
    if mode == '1 maand':
        dates = generate_dates_within_last_month(1)
    elif mode == '3 maanden':
        dates = generate_dates_within_last_month(3)
    elif mode == '6 maanden':
        dates = generate_dates_within_last_month(6)
    else:
        dates = generate_dates_within_last_month(6)
