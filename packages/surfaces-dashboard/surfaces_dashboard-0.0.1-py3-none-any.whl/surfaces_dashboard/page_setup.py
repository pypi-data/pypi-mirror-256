import streamlit as st


def page_setup():
    st.set_page_config(layout="wide")

    hide_streamlit_style = """
    <style>
        #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    </style>
    """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
