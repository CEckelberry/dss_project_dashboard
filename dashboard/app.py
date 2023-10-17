import streamlit as st
import pandas as pd
import numpy as np
from pandasql import sqldf
import altair as alt
import time

# Initialize connection.
conn = st.experimental_connection("postgresql", type="sql")


st.title("Solar Energy Production vs Greenhouse Gas Emissions in the Benelux Region")

# Perform query.
df = conn.query(
    """
    SELECT * FROM "DSS_Datasets_GHG_Solar_iea_data"
    """,
    ttl="10m",
)

iea_data_benelux = sqldf(
    """
    SELECT Country, Time, Product, Value, Unit
    FROM df
    WHERE "Country" = 'Netherlands' OR "Country" = 'Belgium' OR "Country" = 'Luxembourg' 
    GROUP BY Time, Country, Product, Value, Unit
    """)

solar_filter = iea_data_benelux["Product"] == "Solar"
iea_data_benelux = iea_data_benelux[solar_filter]
iea_data_benelux["Time"] = pd.to_datetime(iea_data_benelux["Time"], format="%B %Y")

st.dataframe(iea_data_benelux)


source = iea_data_benelux

chart = alt.Chart(source).mark_line().encode(
    x='Time:T',
    y=alt.Y('Value:Q').title('GhW'),
    color='Country',
)

st.altair_chart(chart.interactive(), theme="streamlit", use_container_width=True)