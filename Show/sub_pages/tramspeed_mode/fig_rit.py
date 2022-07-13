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
from Run.core.Integration.DataInitialization import save_to_sql

def fig_rit():
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        rit_data = pd.read_excel(uploaded_file)
        
        # 查看是否已处理数据
        rit_db_list = [i[:-3] for i in os.listdir(os.path.join(rootPath, 'DataBase', 'rit')) if '.db' in i]
        # rit数据预处理
        if str((rit_data['datum'][0]).date()) not in rit_db_list:
            # 处理上传的excel文件
            rit_data['time'] = rit_data['datum'].astype('str') + ' ' + rit_data['time'].astype('str')
            rit_data = rit_data.drop(columns=['naam', 'richting', 'haltenr.','haltenaam','punc'], axis=1)
            rit_data = rit_data.dropna(how = 'any')
            rit_data = rit_data.astype({'volgnummer': 'int32', 'voertuig': 'int32', 'ritnummer': 'int32', 'lijn': 'int32'})
            rit_data['time'] = pd.to_datetime(rit_data.time, format='%Y-%m-%d %H:%M:%S')
            rit_list = list(set(rit_data.ritnummer.to_list()))
            date_dict = {'today': str((rit_data['datum'][0]).date()), 'yesterday': str((rit_data['datum'][0] - timedelta(days=1)).date())}
            # 匹配数据库
            speed_data_1 = st_get_alldata_from_db(date_dict.get('today'), path='snelheid')
            speed_data_2 = st_get_alldata_from_db(date_dict.get('yesterday'), path='snelheid')
            speed_data = {key: pd.concat([speed_data_1[key], speed_data_2[key]]) for key in speed_data_1}
            
            # 匹配ritnummer到数据库
            for i in rit_list:
                rit_nummer = i
                single_rit = rit_data[rit_data['ritnummer'] == rit_nummer]
                voertuig_nummer = single_rit.iloc[[0]].voertuig.tolist()[0]
                rit_start = single_rit[single_rit['volgnummer'] == single_rit['volgnummer'].min()]['time'].tolist()[0]
                rit_end = single_rit[single_rit['volgnummer'] == single_rit['volgnummer'].max()]['time'].tolist()[0]
                for key, value in speed_data.items():
                    value.loc[(value['<afmelden> wagen'] == voertuig_nummer)&(value['hfk_in'] >= rit_start) & (value['hfk_in'] <= rit_end), 'ritnummer'] = rit_nummer
  
            save_to_sql(date_dict.get('today'), speed_data, path='rit')
        else:
            speed_data = st_get_alldata_from_db(str((rit_data['datum'][0]).date()), path='rit')
            
        # website contain
        # 数据可视化
        all_speed_data = pd.concat(list(speed_data.values()))
        
        st.dataframe(all_speed_data.dropna(how='any'))
