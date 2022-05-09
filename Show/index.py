# ！/usr/bin/python3
# coding:utf-8
from collections import OrderedDict

import pages
import streamlit as st
from core import GetData
from streamlit.logger import get_logger

# set page size

st.set_page_config(
    layout="wide",
    page_title="HTM",
    page_icon="https://www.htm.nl/typo3conf/ext/htm_template/Resources/Public/img/favicon/favicon-16x16.png",
)
LOGGER = get_logger(__name__)

# Dictionary of
# demo_name -> (demo_function, demo_description)
PAGES = OrderedDict(
    [
        ("Welkom", (pages.intro, None)),
        (
            "Tram snelheid",
            (
                pages.tram_speed,
                """
            Deze pagina toont de tram snelheid
            """,
            ),
        ),
        (
            "Wissel schakelen",
            (
                pages.st_wissel_schakel,
                """
                    Deze pagina toont de aantal schakelen van wissels
                    """,
            ),
        ),
        (
            "All data",
            (
                pages.all_data,
                """
                    Deze pagina toont alle data van wissel status
                    """,
            ),
        ),
        (
            "Storing data",
            (
                pages.st_storingdata,
                """
                    Deze pagina toont alle storing data van wissel status
                    """,
            ),
        ),
        (
            "Unknow storing",
            (
                pages.st_unknowstoring,
                """
                    Deze pagina toont alle storing data van wissel status
                    """,
            ),
        ),
        (
            "All storing",
            (
                pages.st_all_storing,
                """
                    Deze pagina toont alle storing data van wissel status
                    """,
            ),
        ),
    ]
)


def run():
    page_name = st.sidebar.selectbox("Kies een pagina", list(PAGES.keys()), 0)
    page = PAGES[page_name][0]
    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    if page_name == "Welkom":
        st.write("# Welkom bij de HTM automatische analyse-app")
        page()
    elif page_name == "Intro" or page_name == "Wissel storingen":
        page()
    elif page_name == "Tram snelheid":
        all_table_name = GetData.get_data_name(path="snelheid")
        all_table_name.sort(reverse=True)
        default_table = all_table_name[:1]
        select_data = st.sidebar.multiselect(
            "Selecteer gegevens om te analyseren", all_table_name, default_table
        )
        page(select_data)
    elif page_name == "Wissel schakelen":
        all_table_name = GetData.get_data_name(path="schakelen")
        all_table_name.sort(reverse=True)
        default_table = all_table_name[:1]
        select_data = st.sidebar.multiselect(
            "Selecteer gegevens om te analyseren", all_table_name, default_table
        )
        page(select_data)
    elif page_name == "Storing data":
        all_table_name = GetData.get_data_name(path="storing")
        all_table_name.sort(reverse=True)
        default_table = all_table_name[:1]
        select_data = st.sidebar.multiselect(
            "Selecteer gegevens om te analyseren", all_table_name, default_table
        )
        page(select_data)
    elif page_name == "Unknow storing":
        all_table_name = GetData.get_data_name(path="unknow_storing")
        all_table_name.sort(reverse=True)
        default_table = all_table_name[:1]
        select_data = st.sidebar.multiselect(
            "Selecteer gegevens om te analyseren", all_table_name, default_table
        )
        page(select_data)
    elif page_name == "All storing":
        all_table_name = GetData.get_data_name(path="all_storing")
        all_table_name.sort(reverse=True)
        default_table = all_table_name[:1]
        select_data = st.sidebar.multiselect(
            "Selecteer gegevens om te analyseren", all_table_name, default_table
        )
        page(select_data)

    else:
        st.markdown("# %s" % page_name)
        desc = PAGES[page_name][1]
        if desc:
            st.write(desc)
        all_table_name = GetData.get_data_name()
        all_table_name.sort(reverse=True)
        default_table = all_table_name[:1]
        select_data = st.sidebar.multiselect(
            "Selecteer gegevens om te analyseren", all_table_name, default_table
        )
        page(select_data)


if __name__ == "__main__":
    run()