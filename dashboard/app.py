import streamlit as st
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title
from solar_production import solar_production
from emissions import ghg_emissions

# Optional -- adds the title and icon to the current page
add_page_title("Solar Energy Production vs Greenhouse Gas Emissions in the Benelux", layout="wide")

sidebar()

# Specify what pages should be shown in the sidebar
show_pages(
    [
        Page("app.py", "Solar Production vs GhG Emissions", ":city_sunrise:"),
        Page("page2.py", "Forest and Land", ":deciduous_tree:"),
        Page("benefits.py", "National Benefits Energy Transition", ":classical_building:"),
    ]
)

#2 columns for main page
col1, col2, col3 = st.columns([8,1,8])
with col1:
    st.header("Solar Production Output Benelux Region")
    solar_production()
with col2:
    st.header(" ")
with col3:
    st.header("Greenhouse Gas Emissions Benelux Region")
    ghg_emissions()