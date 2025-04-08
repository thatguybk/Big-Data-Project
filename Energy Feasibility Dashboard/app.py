import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Natural Gas Environmental Impact", layout="wide")

# Load data

price_df = pd.read_csv("data/Natural_Gas_Import_Price.csv", skiprows=2, parse_dates=["Date"])
quantity_df = pd.read_csv("data/Natural_Gas_Import_Quantity.csv", skiprows=2, parse_dates=["Date"])

st.title(" Natural Gas Environmental Impact Dashboard")
st.markdown("Explore the effects of natural gas use on the environment in the U.S.")

price_df["Year"] = price_df["Date"].dt.year

gas_price_df = price_df.sort_values("Year")

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

# Show raw data
with st.expander("View Raw Data"):
    st.subheader("Price Data")
    st.write(price_df)
    st.subheader("Quantity Data")
    st.write(quantity_df)

st.write("Price Data Columns:", price_df.columns.tolist())
st.write("Quantity Data Columns:", quantity_df.columns.tolist())

# Merge on common column (e.g., Date or Month)
# Adjust column names as necessary
merged_df = pd.merge(price_df, quantity_df, on="Date")

# Rename for clarity (optional)
""" merged_df.rename(columns={
    "Import Price (USD/MMBtu)": "Price",
    "Import Quantity (Million Cubic Meters)": "Quantity"
}, inplace=True) """

# Multiply to get total cost
merged_df["Total Import Cost"] = merged_df["Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)"] * merged_df["U.S. Natural Gas Imports (MMcf)"]

# Multiply to calculate total cost
merged_df["Total Import Cost"] = merged_df["Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)"] * merged_df["U.S. Natural Gas Imports (MMcf)"]


st.write(merged_df.columns.tolist())  # TEMPORARY: See all column names
st.write(merged_df)  # Optional: View full DataFrame


# Show computed result
st.subheader("Total Import Cost")
st.write(merged_df[["Date", "Total Import Cost"]])

# Sort the data if needed (e.g., by Date)
merged_df = merged_df.sort_values("Date")

# Streamlit Bar Chart
st.subheader("Total Natural Gas Import Cost (Bar Chart)")
st.bar_chart(data=merged_df, x="Date", y="Total Import Cost")

# Optional: Streamlit Line Chart
st.subheader("Total Natural Gas Import Cost (Line Chart)")
st.line_chart(data=merged_df, x="Date", y="Total Import Cost")

