import streamlit as st
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title

sidebar()

def solar_panels():
    add_page_title("Number of Solar Panels Needed", layout="wide")
    

    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    df = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_energy_production_benelux"
        """
    )

    st.dataframe(df)

solar_panels()