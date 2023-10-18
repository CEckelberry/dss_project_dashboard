import streamlit as st
import pandas as pd
import numpy as np
from pandasql import sqldf
import altair as alt
from iea_data import iea_data
from sidebar import sidebar

st.title("Solar Energy Production vs Greenhouse Gas Emissions in the Benelux Region")
sidebar()
iea_data()