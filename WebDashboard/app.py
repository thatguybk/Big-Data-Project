import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

st.set_page_config(page_title="Natural Gas Environmental Impact", layout="wide")

# Load data

price_df = pd.read_csv("data/Natural_Gas_Import_Price.csv", skiprows=2, parse_dates=["Date"])
price_df["Date"] = pd.to_datetime(price_df["Date"])


quantity_df = pd.read_csv("data/Natural_Gas_Import_Quantity.csv", skiprows=2, parse_dates=["Date"])
quantity_df["Date"] = pd.to_datetime(quantity_df["Date"])


quantityProduced_df = pd.read_csv("data/Natural_Gas_Plant_Processing.csv", skiprows=6, sep=None, engine="python")
quantityProduced_df["Month"] = pd.to_datetime(quantityProduced_df["Month"], errors="coerce")
quantityProduced_df = quantityProduced_df.sort_values("Month", ascending=False).reset_index(drop=True)
quantityProduced_df = quantityProduced_df[quantityProduced_df["Month"].dt.year > 1989]
print(quantityProduced_df.head())
print(quantityProduced_df.dtypes)


temp_df = pd.read_csv("data/TempData.csv", skiprows=3)
#df = temp_df.rename(columns={"Value": "Temperature (f)"})
temp_df["Date"] = temp_df["Date"].astype(str)  # Convert to string
temp_df["Date"] = pd.to_datetime(temp_df["Date"], format="%Y%m")  # Convert to datetime
temp_df = temp_df[temp_df["Date"].dt.year > 1989]
#print(temp_df.head())

solar_df = pd.read_csv("data/Solar_Energy_Generation.csv", skiprows=4)
# Convert 'Month' column to datetime
solar_df["Month"] = pd.to_datetime(solar_df["Month"])
# Sort the DataFrame by date
solar_df = solar_df.sort_values("Month")
solar_df = solar_df.reset_index(drop=True)
solar_df =solar_df[solar_df["Month"].dt.year < 2025]

# Preview the result
#print(solar_df.tail())

st.title(" Renewable Energy Feasiblity Dashboard (USA)")
st.markdown("This dashboard provides insights into the environmental impact of natural gas imports in the United States and the associated economic strain of implementing Solar power generation.") 
st.markdown("Our goal is to explore the economic implications of natural gas imports and solar power generation in the US. We will analyze the trends in natural gas prices and quantities imported, as well as the growth of solar energy generation over time. This analysis will help us understand the potential benefits of transitioning to renewable energy sources. We will also explore at what point (year) it would make the most sense to impliment Solar Power in the form of Photovoltaic cells, to match the energy consumed.")



# Filter to only include data after 1985
###price_df = price_df[price_df["Date"].dt.year > 2015]
quantity_df = quantity_df[quantity_df["Date"].dt.year >= 1998]

gas_price_df = price_df.sort_values("Date")
quantity_df = quantity_df.sort_values("Date").reset_index(drop=True)

gas_price_df = gas_price_df[gas_price_df["Date"].dt.year > 1998]
temp_df = temp_df[temp_df["Date"].dt.year > 1998]

st.markdown("There are many Factors that affect the price of natural gas imports including weather, temperature, natural desasters and other events that disrupt supply chains. We will explore these factors in the following sections.")

# Create bar chart
st.subheader("Natural Gas Import Price (1999 - 2024)")
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

st.subheader("Temperature (1999 - 2025)")
st.markdown("This chart illustrates the temperature trend in the US from 1990 to 2025.")
fig = px.line(temp_df, x="Date", y="Value")
fig.update_layout(yaxis_title="Temperature (f)", xaxis_title="Date")
# Display in Streamlit
st.plotly_chart(fig)
st.markdown(" The data shows a steady increase in temperature, which is consistent with the global trend of rising temperatures due to climate change. The data also shows seasonal variations, with higher temperatures in the summer months and lower temperatures in the winter months. As temerature decreases the demand for natural gas increases, leading to higher prices. The data shows a clear correlation between temperature and the price of natural gas imports. For example, in January 2014, the average temperature in the US was significantly lower than in previous years, leading to a spike in natural gas prices. This trend is also evident in the winter of 2000/2001, when low temperatures led to increased demand for natural gas and higher prices.")

# Show raw data
with st.expander("View Raw Data"):
    st.subheader("Price Data")
    st.write(price_df)
    st.subheader("Quantity Data")
    st.write(quantity_df)



truncated_price_df = price_df
truncated_price_df["Date"] = pd.to_datetime(price_df["Date"]).dt.to_period("M").dt.to_timestamp()
merged_df_1 = pd.merge(temp_df, truncated_price_df, on="Date", how="inner")
merged_df_1.rename(columns={"Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)": "Gas Price"}, inplace=True)
#print(truncated_price_df.head())

# Calculate correlation matrix (for numeric columns only)
correlation = merged_df_1.select_dtypes(include=["float64", "int64"]).corr()

# Plot the correlation heatmap
st.subheader("Correlation Between Temperature and Natural Gas Price")
fig, ax = plt.subplots(figsize=(4,2))
sns.heatmap(correlation, annot=True, cmap="crest", fmt=".2f", ax=ax)
st.pyplot(fig)



# --- Add Season Column ---
def get_season(month):
    if month in [12, 1, 2, 3]:
        return "Winter"
    elif month in [4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

merged_df_1["Season"] = merged_df_1["Date"].dt.month.apply(get_season)

# --- Calculate correlations for each season ---
season_correlations = merged_df_1.groupby("Season")[["Value", "Gas Price"]].corr().iloc[0::2, -1].reset_index()

# Display season correlations
print("Seasonal correlations between temperature and gas price:")
print(season_correlations)

# Visualize as bar chart
fig, ax = plt.subplots(figsize=(3,2))
sns.barplot(data=season_correlations, x="Season", y="Gas Price", palette="inferno", ax=ax)
ax.set_title("Correlation Between Temperature and Gas Price by Season")
ax.set_ylabel("Correlation Coefficient")
ax.set_ylim(-1, 1)
ax.axhline(0, color='gray', linestyle='--')

# Display in Streamlit
st.pyplot(fig)


st.markdown("The correlation between temperature and natural gas price is significant, with a correlation coefficient of {:.3f}. This indicates that as temperature decreases, the price of natural gas increases. The data also shows a seasonal pattern, with higher prices in the winter months when demand for natural gas is highest.".format(correlation.loc['Value', 'Gas Price']))

st.markdown("The correlation coefficient for each season is as follows:")
for season, corr in zip(season_correlations['Season'], season_correlations['Gas Price']):
    st.markdown(f"- **{season}:** {corr:.3f}")

st.markdown("The correlation is skewed due to other factors, such as natural disasters and supply chain disruptions, affecting the price of natural gas.")



# Merge on common column (e.g., Date or Month)
# Adjust column names as necessary

quantity_df["Date"] = pd.to_datetime(quantity_df["Date"]).dt.to_period("M").dt.to_timestamp()

merged_df = pd.merge(price_df, quantity_df, on="Date", how="inner")


# Multiply to calculate total cost
merged_df["Total Import Cost"] = merged_df["Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)"] * (merged_df["U.S. Natural Gas Imports (MMcf)"]* 1000)

# Sort the data if needed (e.g., by Date)
merged_df = merged_df.sort_values("Date")

#Quantity of Natural Gas Imported over the years

st.subheader("U.S. Natural Gas Imports (1989 - 2024)")
fig = px.line(
    merged_df,
    x="Date",
    y="U.S. Natural Gas Imports (MMcf)",
    title="U.S. Natural Gas Imports Over the Years",
    labels={"U.S. Natural Gas Imports (MMcf)": "Natural Gas Imported (MMcf)"}
)

# Display the chart in Streamlit
st.plotly_chart(fig)
st.markdown("The quantity of natural gas imported into the US has fluctuated over the years, with notable peaks and troughs. The data shows a steady increase in the quantity of natural gas imported until 2008, reflecting the growing demand for natural gas in the US. After 2008 the US increased its domestic production of natural gas. The data also shows seasonal variations, with higher imports in the winter months and lower imports in the summer months. This trend is consistent with the seasonal demand for natural gas.")


st.subheader("Natural Gas Production Data (1990 - 2024)")
fig = px.line(quantityProduced_df, x="Month", y="U.S. Natural Gas Plant Liquids Production MMcf")
fig.update_layout(yaxis_title="Natural Gas Produced (Million Cublic Feat MMcf)", xaxis_title="Date")
# Display in Streamlit
st.plotly_chart(fig)


#correlation between imports and production
quantityProduced_df.rename(columns={"Month": "Date"}, inplace=True)
merged_df_2 = pd.merge(quantity_df, quantityProduced_df, on="Date", how="inner")

merged_df_renamed = merged_df_2.rename(columns={
    "U.S. Natural Gas Imports (MMcf)": "Imports (MMcf)",
    "U.S. Natural Gas Plant Liquids Production MMcf": "Produced (MMcf)"
})

#Only numic columns to be correlated
correlation_data = merged_df_renamed.select_dtypes(include='number')
# Compute correlation matrix
correlation_matrix = correlation_data.corr()

# Plot using seaborn
st.subheader("Correlation Matrix: Natural Gas Imports vs Production")
fig, ax = plt.subplots(figsize=(4, 2))
sns.heatmap(correlation_matrix, annot=True, cmap="crest", ax=ax)
st.pyplot(fig)
st.markdown(f"The above graphs show a negative correlation of {correlation_matrix.iloc[0, 1]:.2f}. This indicates that as the quantity of natural gas imports decreases, the quantity of natural gas produced increases. This trend is consistent with the growing domestic production of natural gas in the US, which has led to a decrease in imports.")


#Total cost to import over the years
st.subheader("Total Natural Gas Import Cost (1989 - 2024)")
fig = px.line(
    merged_df,
    x="Date",
    y="Total Import Cost",
    #title="Total Natural Gas Import Cost (1989 - 2024)",
    labels={"Total Import Cost": "Total Import Cost (USD)"}
)



# Display in Streamlit
st.plotly_chart(fig)

st.markdown("By multiplying the price of natural gas by the quantity imported, we can see the total cost to import natural gas. The price of natural gas is listed in the dataset as per thousand cubic feet ($/Mcf), and the quantity dataset displays the values int the unit of million cubic feet (MMcf). To normalize these values, we multiply the quantity by 1000 then multiply the result by the cost to get the total cost incurred by the US for importing natural gas.")


st.subheader("Solar Energy Generation Data (2001 - 2024)")
st.write(solar_df.head())

# Show a line chart using Streamlit
st.subheader("Solar Energy Generation Over Time")
st.markdown("This chart illustrates the solar energy generation in the US from 2001 to 2024. The data shows a steady increase in solar energy generation, reflecting the growing adoption of renewable energy sources.")
st.line_chart(data=solar_df, x="Month", y=solar_df.columns[1])


