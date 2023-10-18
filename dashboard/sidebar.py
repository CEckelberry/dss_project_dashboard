import streamlit as st
from PIL import Image
import time

def sidebar():

    with st.sidebar:
        image = Image.open("./images/sidebar_illustration.jpg")
        st.image(image, output_format="auto")
        with st.echo():
            st.write("This code will be printed to the sidebar.")

        with st.spinner("Loading..."):
            time.sleep(5)
        st.success("Done!")

