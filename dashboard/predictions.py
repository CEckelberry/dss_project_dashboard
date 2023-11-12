import altair as alt
import streamlit as st
import pandas as pd
import altair as alt
from sidebar import sidebar
from st_pages import Page, show_pages, add_page_title
from neuralprophet import NeuralProphet



def predictions():

    add_page_title("Predictions for Solar Production", layout="wide")

    sidebar()
    # Initialize connection.
    conn = st.experimental_connection("postgresql", type="sql")
    # Perform query.
    iea_data = conn.query(
        """
        SELECT * FROM "DSS_Datasets_GHG_Solar_iea_data"
        """
    )

    # Filter data
    countries = ['Netherlands', 'Belgium', 'Luxembourg']
    solar_filter = iea_data["Product"] == "Solar"
    country_filter = iea_data["Country"].isin(countries)
    iea_data = iea_data[solar_filter & country_filter]

    # Process data
    iea_data["Time"] = pd.to_datetime(iea_data["Time"], format="%B %Y")
    iea_data['Value'] = pd.to_numeric(iea_data['Value'], errors='coerce')
    data = iea_data.sort_values(by=["Time"], ascending=True)
    data = data.loc[data['Time'] >= '2017-01-01']

    # Separate data by country
    
    NLdata = data[data["Country"] == "Netherlands"]
    BEdata = data[data["Country"] == "Belgium"]
    LUXdata = data[data["Country"] == "Luxembourg"]



    NLdatamin = NLdata.rename(columns={"Time": 'ds', 'Value': 'y'})
    BEdatamin = BEdata.rename(columns={"Time": 'ds', 'Value': 'y'})
    LUXdatamin = LUXdata.rename(columns={"Time": 'ds', 'Value': 'y'})

    BENE = pd.concat([NLdatamin, BEdatamin]).groupby(['ds']).sum().reset_index()
    BENELUXdatamin = pd.concat([BENE, LUXdatamin]).groupby(['ds']).sum().reset_index()
    st.write(BENELUXdatamin.dtypes)
    BENELUXdatamin = BENELUXdatamin.drop(columns=['Country', 'Balance', 'Product', 'Unit'])

    mBENELUX = NeuralProphet()
    mBENELUX.fit(BENELUXdatamin)

    df_futureBENELUX = mBENELUX.make_future_dataframe(BENELUXdatamin, periods=48)
    BENELUXforecast = mBENELUX.predict(df_futureBENELUX)

    BENELUXforecast.rename(columns={'yhat1': 'y'}, inplace=True)

    BeneluxPred = pd.concat([BENELUXdatamin, BENELUXforecast])

    st.subheader("BENELUX Prediction Data")
    st.write(BeneluxPred)

       
    

predictions()