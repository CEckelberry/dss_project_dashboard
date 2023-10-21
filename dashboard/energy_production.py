import altair as alt
import streamlit as st
import pandas as pd
import altair as alt
from st_pages import Page, show_pages, add_page_title
from sidebar import sidebar

add_page_title("Energy Production", layout="wide")

def energy_production():
    sidebar()
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    national_benefitdf = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_Solar_Potential_National_Income_Benefit_from_A"
        """
    )

energy_production()