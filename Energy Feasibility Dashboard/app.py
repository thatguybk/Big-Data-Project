import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Natural Gas Environmental Impact", layout="wide")

# Load data

price_df = pd.read_csv("data/Natural_Gas_Import_Price.csv", skiprows=2, parse_dates=["Date"])
quantity_df = pd.read_csv("data/Natural_Gas_Import_Quantity.csv", skiprows=2, parse_dates=["Date"])

st.title(" Natural Gas Environmental Impact Dashboard")
st.markdown("This dashboard provides insights into the environmental impact of natural gas imports in the United States and the associated economic strain of implementing Solar power generation.") 

price_df["Date"] = pd.to_datetime(price_df["Date"])
quantity_df["Date"] = pd.to_datetime(quantity_df["Date"])

# Filter to only include data after 1985
###price_df = price_df[price_df["Date"].dt.year > 2015]
quantity_df = quantity_df[quantity_df["Date"].dt.year > 1989]

gas_price_df = price_df.sort_values("Date")

# Create bar chart
fig = px.bar(
    gas_price_df,
    x="Date",
    y="Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)",
    title="Natural Gas Prices Over the Years",
    labels={
        "Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)": "Price (USD per 1000 Cubic Feet)",
        "Date": "Date"
    },
    color_discrete_sequence=["steelblue"]
)

# Show chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

#Paragraph of Natural Gas prices every month from 1998 to 2024
st.markdown("Here we can see the trends of the price to import Natural gas into the US from 1998 to 2004. The price of natural gas has fluctuated over the years, with notable peaks and troughs. This data is crucial for understanding the economic implications of natural gas imports and the potential benefits of transitioning to renewable energy sources.")

# Show raw data
with st.expander("View Raw Data"):
    st.subheader("Price Data")
    st.write(price_df)
    st.subheader("Quantity Data")
    st.write(quantity_df)

##st.write("Price Data Columns:", price_df.columns.tolist())
##st.write("Quantity Data Columns:", quantity_df.columns.tolist())

# Merge on common column (e.g., Date or Month)
# Adjust column names as necessary
merged_df = pd.merge(price_df, quantity_df, on="Date")

# Multiply to get total cost
merged_df["Total Import Cost"] = merged_df["Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)"] * merged_df["U.S. Natural Gas Imports (MMcf)"]

# Multiply to calculate total cost
merged_df["Total Import Cost"] = merged_df["Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)"] * merged_df["U.S. Natural Gas Imports (MMcf)"]


# Sort the data if needed (e.g., by Date)
merged_df = merged_df.sort_values("Date")





# Streamlit Bar Chart
##st.subheader("Total Natural Gas Import Cost (Bar Chart)")
##st.bar_chart(data=merged_df, x="Date", y="Total Import Cost")

# Optional: Streamlit Line Chart
st.subheader("Total Natural Gas Import Cost (1989 - 2024)")
st.markdown("By multiplying the price of natural gas by the quantity imported, we can see the total cost incurred by the US for importing natural gas. ")
st.line_chart(data=merged_df, x="Date", y="Total Import Cost")

