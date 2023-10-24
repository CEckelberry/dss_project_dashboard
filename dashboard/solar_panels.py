import streamlit as st
import pandas as pd
import altair as alt
from st_pages import Page, show_pages, add_page_title
from sidebar import sidebar 

add_page_title("This is how many solar panels are needed to fully replace fossil fuels", layout="wide")

def solar_panels():
    sidebar()

    st.markdown(
        """
        <div style='text-align: justify;'>

        <p style='font-size: 18px;'>An estimation of the number of solar panels needed to fully replace fossil fuels is presented below.</p>

        <p style='font-size: 18px;'>One significant aspect that directly influences solar panel performance is its wattage, and it will affect how many panels are needed. The higher the wattage, the more power a panel can generate.</p>

        <p style='font-size: 18px;'>Most residential solar panels have ratings of 250 to 400 watts. The most efficient solar panels on the market are 370- to 445-watt models. The higher the wattage rating, the higher the output. In turn, the fewer panels you might be needed.</p>

        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    solar_panels_df = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_energy_production_benelux" 
        """
    )

    # Filtering data for fossil fuels and solar
    fossil_fuels_df = solar_panels_df[solar_panels_df['Product'].str.contains('Fuels|Coal|Oil|Gas', case=False, regex=True)]
    solar_df = solar_panels_df[solar_panels_df['Product'].str.contains('Solar', case=False, regex=True)]

    # Convert 'Value' column to numeric
    fossil_fuels_df['Value'] = pd.to_numeric(fossil_fuels_df['Value'])
    solar_df['Value'] = pd.to_numeric(solar_df['Value'])

    # Calculate the total electricity production from fossil fuels and solar panels
    total_fossil_fuels = round(fossil_fuels_df['Value'].sum(), 2)
    total_solar_energy = round(solar_df['Value'].sum(), 2)

    # Conversion constant
    gwh_to_wh = 1000000000 # GWh to watt-hours

    # Convert total electricity production to watt-hours
    total_fossil_fuels_watts = total_fossil_fuels * gwh_to_wh
    total_solar_energy_watts = total_solar_energy * gwh_to_wh

    # Calculate the number of solar panels needed, assuming that one solar panel produces 400 watt energy
    number_of_solar_panels = int(total_fossil_fuels_watts / 400)

    # Slider for selecting the wattage
    selected_wattage = st.slider('Please select the wattage (between 250 and 500)', 250, 500, 400)

    # Calculate the number of solar panels needed, based on the selected wattage
    number_of_solar_panels = int(total_fossil_fuels_watts / selected_wattage)

    st.write(f"Based on the data and the selected wattage ({selected_wattage} watts), the number of solar panels needed to replace fossil fuels is: ", number_of_solar_panels)

    colors = ['#17BEBB', '#3590F3']

    st.subheader("Comparison of Electricity Production from Fossil Fuels and Solar Energy")

    data = pd.DataFrame({
        'Energy Source': ['Fossil Fuels', 'Solar Energy'],
        'Electricity Production (GWh)': [total_fossil_fuels, total_solar_energy]
    })
    
    chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('Electricity Production (GWh)', title='Electricity Production (GWh)'),
    y=alt.Y('Energy Source', title=None),
    color=alt.Color('Energy Source', scale=alt.Scale(range=['#17BEBB', '#3590F3']))
    ).properties(
        width=600,
        height=400
    )

    st.write(chart)

solar_panels()
