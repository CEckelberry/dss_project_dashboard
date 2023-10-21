import streamlit as st
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title

def solar_panels():
    add_page_title("Number of Solar Panels Needed", layout="wide")
    sidebar()


solar_panels()