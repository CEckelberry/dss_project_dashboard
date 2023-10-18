import streamlit as st
import pandas as pd
from pandasql import sqldf
import altair as alt

def iea_data():
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
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
        """
        )

    solar_filter = iea_data_benelux["Product"] == "Solar"
    iea_data_benelux = iea_data_benelux[solar_filter]
    iea_data_benelux["Time"] = pd.to_datetime(iea_data_benelux["Time"], format="%B %Y")
    #st.dataframe(iea_data_benelux)
    source = iea_data_benelux


    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection_point(nearest=True, on='mouseover',
                            fields=['Value'], empty=False)

    line = alt.Chart(source, title="Solar Energy Production over Time in the Benelux").mark_line(interpolate='basis').encode(
        x='Time:T',
        y=alt.Y('Value:Q').title('GhW'),
        color='Country',
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(source).mark_point().encode(
        x='Time:T',
        opacity=alt.value(0),
    ).add_params(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'Value:Q', alt.value(' '))
    )
    # Draw a rule at the location of the selection
    rules = alt.Chart(source).mark_rule(color='gray').encode(
        x='Time:T',
    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data
    chart = alt.layer(
        line, selectors, points, rules, text
    ).properties(
        width=1000, height=650
    )

    st.altair_chart(chart, theme="streamlit")
