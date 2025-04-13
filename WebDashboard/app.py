import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Natural Gas Environmental Impact", layout="wide")

# Load data

price_df = pd.read_csv("data/Natural_Gas_Import_Price.csv", skiprows=2, parse_dates=["Date"])
quantity_df = pd.read_csv("data/Natural_Gas_Import_Quantity.csv", skiprows=2, parse_dates=["Date"])
# Load CSV, skipping the first 2 rows

temp_df = pd.read_csv("data/TempData.csv", skiprows=3)
df = temp_df.rename(columns={"Value": "Temperature (f)"})
temp_df["Date"] = temp_df["Date"].astype(str)  # Convert to string
temp_df["Date"] = pd.to_datetime(temp_df["Date"], format="%Y%m")
temp_df = temp_df[temp_df["Date"].dt.year > 1989]
#temp_df["Date"] = temp_df.sort_values("Date").reset_index(drop=True)
print(temp_df.head())

solar_df = pd.read_csv("data/Solar_Energy_Generation.csv", skiprows=4)
# Convert 'Month' column to datetime
solar_df["Month"] = pd.to_datetime(solar_df["Month"])
# Sort the DataFrame by date
solar_df = solar_df.sort_values("Month")
# Optional: Reset index
solar_df = solar_df.reset_index(drop=True)
solar_df =solar_df[solar_df["Month"].dt.year < 2025]

# Preview the result
#print(solar_df.tail())

st.title(" Renewable Energy Feasiblity Dashboard (USA)")
st.markdown("This dashboard provides insights into the environmental impact of natural gas imports in the United States and the associated economic strain of implementing Solar power generation.") 
st.markdown("Our goal is to explore the economic implications of natural gas imports and solar power generation in the US. We will analyze the trends in natural gas prices and quantities imported, as well as the growth of solar energy generation over time. This analysis will help us understand the potential benefits of transitioning to renewable energy sources. We will also explore at what point (year) it would make the most sense to impliment Solar Power in the form of Photovoltaic cells, to match the energy consumed.")


price_df["Date"] = pd.to_datetime(price_df["Date"])
quantity_df["Date"] = pd.to_datetime(quantity_df["Date"])

# Filter to only include data after 1985
###price_df = price_df[price_df["Date"].dt.year > 2015]
quantity_df = quantity_df[quantity_df["Date"].dt.year > 1989]

gas_price_df = price_df.sort_values("Date")


st.markdown("There are many Factors that affect the price of natural gas imports, including: weather, temperature, natural desasters and other events that disrupt supply chains. We will explore these factors in the following sections.")



# Create bar chart
st.subheader("Natural Gas Import Price (1989 - 2024)")
#st.markdown("Here we can see the trends of the price to import Natural gas into the US from 1998 to 2004.")

fig = px.bar(
    gas_price_df,
    x="Date",
    y="Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)",
    labels={
        "Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)": "Price (USD per 1000 Cubic Feet)",
        "Date": "Date"
    },
    color_discrete_sequence=["steelblue"]
)

# Show chart in Streamlit
st.plotly_chart(fig, use_container_width=True)


st.markdown("The price of natural gas has fluctuated over the years, with notable peaks and troughs. This data is crucial for understanding the economic implications of natural gas imports and the potential benefits of transitioning to renewable energy sources. In September 2005, according to the U.S. Energy Information Administration (EIA), the price of natural gas imports was 6.00 per thousand cubic feet (Mcf). This was a significant increase from the previous year, when the price was around 4.00 per Mcf. The increase in price was attributed to several factors, including increased demand for natural gas due to Hurricane Katrina and other weather-related events that disrupted supply chains.")

st.subheader("Temperature (1990 - 2024)")
st.markdown("This chart illustrates the temperature trend in the US from 1990 to 2024. The data shows a correlation between temperature and the price of natural gas imports.")
fig = px.line(temp_df, x="Date", y="Value")
fig.update_layout(yaxis_title="Temperature (f)", xaxis_title="Date")
# Display in Streamlit
st.plotly_chart(fig)
st.markdown("As temerature decreases the demand for natural gas increases, leading to higher prices. The data shows a clear correlation between temperature and the price of natural gas imports. For example, in January 2014, the average temperature in the US was significantly lower than in previous years, leading to a spike in natural gas prices. This trend is also evident in the winter of 2000/2001, when low temperatures led to increased demand for natural gas and higher prices.")
#st.markdown("The high cost of natural gas in the winter of 2000/2001 is due to the low temperature, increating demand for natual gas. The data also explains the spike of natural gas price in Febuary 2014 due to the low temeratures in the US.")

#Paragraph of Natural Gas prices every month from 1998 to 2024

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


st.subheader("Solar Energy Generation Data (2001 - 2024)")
st.write(solar_df.head())

# Show a line chart using Streamlit
st.subheader("Solar Energy Generation Over Time")
st.markdown("This chart illustrates the solar energy generation in the US from 2001 to 2024. The data shows a steady increase in solar energy generation, reflecting the growing adoption of renewable energy sources.")
st.line_chart(data=solar_df, x="Month", y=solar_df.columns[1])

