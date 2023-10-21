import altair as alt
import streamlit as st
import pandas as pd
import altair as alt
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title

def predictions():

    add_page_title("Predictions for Solar Production", layout="wide")

    sidebar()
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    national_benefitdf = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_Solar_Potential_National_Income_Benefit_from_A"
        """
    )

predictions()