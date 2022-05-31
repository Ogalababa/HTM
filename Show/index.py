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
            "Storing data",
            (
                pages.st_storing,
                """
                    Deze pagina toont alle storing data van wissel status
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
    ]
)


def run():
    # st.sidebar.warning('De website is nu in onderhouden, het hele proces duurt ongeveer 10 minuten')
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
        page()
    elif page_name == "Wissel schakelen":
        page()
    elif page_name == "Storing data":
        page()
    else:
        st.markdown("# %s" % page_name)
        desc = PAGES[page_name][1]
        if desc:
            st.write(desc)

        page()


if __name__ == "__main__":
    run()
