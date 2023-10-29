import streamlit as st
from PIL import Image
from pandasql import sqldf
import pandas as pd
import time

def sidebar():

    with st.sidebar:
        image = Image.open("./images/sidebar_illustration.jpg")
        st.image(image, output_format="auto") 
        # Initialize connection.
        conn = st.experimental_connection("postgresql", type="sql")
        # Perform query.
        dfGHG = conn.query(
            """
            SELECT * FROM "DSS_Datasets_GHG_Solar_National_Greenhouse_Gas_Emissions_Invent"
            """
        )
        # Initialize an empty DataFrame
        progress_df_paris = pd.DataFrame(columns=['Country', 'Progress'])

        paris_agreement = 0.43 #The goal of the Paris agreement is to have a 43% reduction of the GHG by 2030 relative to the GHG emissions in 2019

        # Assuming dfGHG is your DataFrame
        for country in dfGHG['Country'].unique():
            filtered_dfGHG = dfGHG[dfGHG['Country'] == country]
            filtered_dfGHG['2019'] = filtered_dfGHG['2019'].astype(float)
            filtered_dfGHG['2021'] = filtered_dfGHG['2021'].astype(float)
            year_2019 = filtered_dfGHG['2019'].sum().round(4)
            year_2021 = filtered_dfGHG['2021'].sum().round(4)
            target_paris = year_2019 * paris_agreement
            progress_paris = (1 - (target_paris / year_2021)) * 100
            # Create a new DataFrame with each iteration
            temp_df = pd.DataFrame({'Country': [country], 'Progress': [progress_paris]})
            # Append the temporary DataFrame to the main DataFrame
            progress_df_paris = pd.concat([progress_df_paris, temp_df], ignore_index=True)

        # Extract progress values
        netherlands_progress_value = progress_df_paris.loc[progress_df_paris['Country'] == "Netherlands, The", 'Progress'].values[0]
        belgium_progress_value = progress_df_paris.loc[progress_df_paris['Country'] == "Belgium", 'Progress'].values[0]
        luxembourg_progress_value = progress_df_paris.loc[progress_df_paris['Country'] == "Luxembourg", 'Progress'].values[0]

        # Dictionary containing country names and their corresponding percentages
        countries = {
            "Netherlands": netherlands_progress_value,
            "Belgium": belgium_progress_value,
            "Luxembourg": luxembourg_progress_value 
        }

        # Display progress bars for each country
        st.title("Progress To Paris Agreement Greenhouse Gas Reductions")

        for country, percentage in countries.items():
            st.write(f"{country}: {round(percentage, 2)}%")
            st.progress(round(percentage, 2)/ 100)

