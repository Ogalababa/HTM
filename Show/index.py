# ！/usr/bin/python3
# coding:utf-8


import streamlit as st
from streamlit.logger import get_logger
from collections import OrderedDict

from Show.core import GetData
import pages

# set page size

st.set_page_config(
    layout='wide',
    page_title='HTM',
    page_icon='https://www.htm.nl/typo3conf/ext/htm_template/Resources/Public/img/favicon/favicon-16x16.png')
LOGGER = get_logger(__name__)

# Dictionary of
# demo_name -> (demo_function, demo_description)
PAGES = OrderedDict(
    [
        ('Welkom',
         (pages.intro,
          None
          )
         ),

        ('Tram snelheid', (
            pages.tram_speed,
            '''
            Deze pagina toont de tram snelheid
            ''',
        ),
         ),

        ('All data', (
                    pages.all_data,
                    '''
                    Deze pagina toont alle data van wissel status
                    ''',
                ),
                 ),
    ]
)


def run():
    page_name = st.sidebar.selectbox('Kies een pagina', list(PAGES.keys()), 0)
    page = PAGES[page_name][0]
    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    if page_name == 'Welkom':
        st.write('# Welkom bij de HTM automatische analyse-app')
        page()
    elif page_name == 'Intro' or page_name == 'Wissel storingen':
        page()
    elif page_name == 'Tram snelheid':
        all_table_name = GetData.get_data_name(path='snelheid')
        all_table_name.sort(reverse=True)
        default_table = all_table_name[:1]
        select_data = st.sidebar.multiselect('Selecteer gegevens om te analyseren', all_table_name, default_table)
        page(select_data)


    else:
        st.markdown('# %s' % page_name)
        desc = PAGES[page_name][1]
        if desc:
            st.write(desc)
        all_table_name = GetData.get_data_name()
        all_table_name.sort(reverse=True)
        default_table = all_table_name[:1]
        select_data = st.sidebar.multiselect('Selecteer gegevens om te analyseren', all_table_name, default_table)
        page(select_data)


if __name__ == "__main__":
    run()
