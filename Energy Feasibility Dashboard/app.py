import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Natural Gas Environmental Impact", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/Natural_Gas_Import_Price.csv",skiprows=2, parse_dates=["Date"])

df = load_data()

st.title(" Natural Gas Environmental Impact Dashboard")
st.markdown("Explore the effects of natural gas use on the environment in the U.S.")

df["Year"] = df["Date"].dt.year

gas_price_df = df.sort_values("Year")

# Create bar chart
fig = px.bar(
    gas_price_df,
    x="Year",
    y="Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)",
    title="💰 Natural Gas Prices Over the Years",
    labels={
        "Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)": "Price (USD per 1000 Cubic Feet)",
        "Year": "Year"
    },
    color_discrete_sequence=["steelblue"]
)

# Show chart in Streamlit
st.plotly_chart(fig, use_container_width=True)