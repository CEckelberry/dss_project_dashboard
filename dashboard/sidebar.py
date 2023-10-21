import streamlit as st
from PIL import Image
import time

def sidebar():

    with st.sidebar:
        image = Image.open("./images/sidebar_illustration.jpg")
        st.image(image, output_format="auto") 

        # Dictionary containing country names and their corresponding percentages
        countries = {
            "Netherlands": 85,
            "Belgium": 62,
            "Luxembourg": 47
        }

        # Display progress bars for each country
        st.title("Progress To Paris Agreement Greenhouse Gas Reductions")

        for country, percentage in countries.items():
            st.write(f"{country}: {percentage}%")
            st.progress(percentage / 100.0)

