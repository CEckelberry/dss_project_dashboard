import altair as alt
import streamlit as st
import pandas as pd
import altair as alt

def natl_benefits():
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    df = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_Solar_Potential_National_Income_Benefit_from_A"
        """
    )
    st.dataframe(df)
    national_benefitdf = df[df['Percentile'] == 50] #only use one percentile, otherwise everything has two values
    national_benefitdf.set_index(['Country', 'Model', 'Scenario'], inplace=True)
    st.dataframe(national_benefitdf)
    # Filter columns that are valid years (numeric)
    year_columns2 = [col for col in national_benefitdf.columns if col.isdigit()]
    national_benefitdf = national_benefitdf[year_columns2]

    # Stack the DataFrame to create a multi-index Series
    stackednational_benefit = national_benefitdf.stack()

    # Reset the index to convert it back to a DataFrame
    stackednational_benefit = stackednational_benefit.reset_index()

    # Rename the columns
    stackednational_benefit.columns = ['Country', 'Model', 'Scenario', 'Year', 'Damage']

    # Convert the 'Year' column to integers and group them in steps of 10
    stackednational_benefit['Year'] = stackednational_benefit['Year'].astype(int)
    stackednational_benefit['YearGroup'] = (stackednational_benefit['Year'] // 10) * 10

    

    """     # Define the Altair chart
    chart = alt.Chart(stackednational_benefit).mark_bar(
        filled=True,
        cursor='pointer'
    ).encode(
        x=alt.X('Country:O', title='Country', axis=alt.Axis(grid=True, ticks=True, labels=True, labelFlush=False)),
        y=alt.Y('sum(Damage):Q', title='Sum of Damage', axis=alt.Axis(grid=True, ticks=True, labels=True, labelFlush=False)),
        color=alt.Color('Scenario:N', 
                    scale=alt.Scale(range=['#4C78A8', '#F58518', '#E45756', '#72B7B2', '#54A24B', '#EECA3B', 
                                            '#B279A2', '#FF9DA6', '#9D755D', '#BAB0AC']),
                    legend=alt.Legend(symbolOpacity=1),
                    title='Scenario'
                    ),
        opacity=alt.condition(
            alt.not_(alt.selection_interval(encodings=['x'])),
            alt.value(0.3),
            alt.value(1)
        ),
        tooltip=[
            alt.Tooltip('Country:O', title='Country'),
            alt.Tooltip('sum(Damage):Q', title='Sum of Damage', aggregate='sum'),
            alt.Tooltip('Scenario:N')
        ]
    ).add_selection(
        alt.selection_interval(encodings=['x'], name='interval_intervalselection_0') &
        alt.selection_multi(encodings=['color'], name='legend_pointselection_0')
    ).properties(
        width='container',
        height='container'
    )
    """
    # Display the chart using streamlit
    #st.altair_chart(chart, use_container_width=True)

natl_benefits()