import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

st.set_page_config(page_title="Natural Gas Environmental Impact", layout="wide")

# LOAD AND PRE CLEAN DATA

price_df = pd.read_csv("data/Natural_Gas_Import_Price.csv", skiprows=2, parse_dates=["Date"])
price_df = price_df.rename(columns={"Price of U.S. Natural Gas Imports (Dollars per Thousand Cubic Feet)": "Price ($/MCF)"})
price_df["Date"] = pd.to_datetime(price_df["Date"])
price_df["Date"] = pd.to_datetime(price_df["Date"]).dt.to_period("M").dt.to_timestamp()
price_df = price_df.dropna(subset=["Date", "Price ($/MCF)"])



import_df = pd.read_csv("data/Natural_Gas_Import_Quantity.csv", skiprows=2, parse_dates=["Date"])
import_df.columns = ["Date", "Imports (MMcf)"]
import_df["Date"] = pd.to_datetime(import_df["Date"])
import_df["Date"] = pd.to_datetime(import_df["Date"]).dt.to_period("M").dt.to_timestamp()
imports_df = import_df.dropna(subset=["Date", "Imports (MMcf)"])



quantityProduced_df = pd.read_csv("data/Natural_Gas_Plant_Processing.csv", skiprows=6, sep=None, engine="python")
quantityProduced_df = quantityProduced_df.rename(columns={"Month": "Date", "U.S. Natural Gas Plant Liquids Production MMcf": "Production (MMcf)"})
quantityProduced_df.columns = ["Date", "Production (MMcf)"]
quantityProduced_df["Date"] = pd.to_datetime(quantityProduced_df["Date"], errors="coerce")
quantityProduced_df["Date"] = pd.to_datetime(quantityProduced_df["Date"]).dt.to_period("M").dt.to_timestamp()
quantityProduced_df = quantityProduced_df.sort_values("Date", ascending=False).reset_index(drop=True)
quantityProduced_df = quantityProduced_df[quantityProduced_df["Date"].dt.year > 1989]
quantityProduced_df = quantityProduced_df.dropna(subset=["Date", "Production (MMcf)"])



temp_df = pd.read_csv("data/TempData.csv", skiprows=3)
temp_df = temp_df.rename(columns={"Date": "Date", "Value": "Temperature (F)"})
temp_df["Date"] = temp_df["Date"].astype(str)  # Convert to string
temp_df["Date"] = pd.to_datetime(temp_df["Date"], format="%Y%m")  # Convert to datetime
temp_df["Date"] = pd.to_datetime(temp_df["Date"]).dt.to_period("M").dt.to_timestamp()
temp_df = temp_df[temp_df["Date"].dt.year > 1989]
temp_df = temp_df.dropna(subset=["Date", "Temperature (F)"])


solar_df = pd.read_csv("data/Solar_Energy_Generation.csv", skiprows=4)
print(solar_df.columns)
#Standarzing column names
solar_df = solar_df.rename(columns={"Month": "Date", "all utility-scale solar thousand megawatthours": "Solar Generation (1000 MWh)"})
print(solar_df.columns)
solar_df.columns = ["Date", "Solar Generation (1000 MWh)"]
# Convert 'Month' column to datetime
solar_df["Date"] = pd.to_datetime(solar_df["Date"])
# Sort the DataFrame by date
solar_df = solar_df.sort_values("Date")
solar_df = solar_df.reset_index(drop=True)
solar_df =solar_df[solar_df["Date"].dt.year < 2025]
solar_df["Date"] = pd.to_datetime(solar_df["Date"]).dt.to_period("M").dt.to_timestamp()
#Drop NAN values
solar_df = solar_df.dropna(subset=["Date", "Solar Generation (1000 MWh)"])

#MERGE 

allmerged_df = temp_df.merge(price_df, on="Date", how="outer")
allmerged_df = allmerged_df.merge(imports_df, on="Date", how="outer")
allmerged_df = allmerged_df.merge(quantityProduced_df, on="Date", how="outer")
allmerged_df = allmerged_df.merge(solar_df, on="Date", how="outer")
# Sort and reset index
allmerged_df = allmerged_df.sort_values("Date").reset_index(drop=True)
# Drop rows with no useful data
main_cols = ["Temperature (F)", "Price ($/MCF)", "Imports (MMcf)", "Production (MMcf)", "Solar Generation (1000 MWh)"]
allmerged_df = allmerged_df.dropna(subset=main_cols, how="all")

allmerged_df.to_csv("cleaned_merged_dataset.csv", index=False)

allmerged_df = allmerged_df[allmerged_df["Date"].dt.year > 1998]
# Sort and reset index
allmerged_df = allmerged_df.sort_values("Date").reset_index(drop=True)
print(allmerged_df.tail(100))
print(allmerged_df.head(100))
print(allmerged_df.dtypes)






st.title(" Renewable Energy Feasiblity Dashboard (USA)")
st.markdown("This dashboard provides insights into the environmental impact of natural gas imports in the United States and the associated economic strain of implementing Solar power generation.") 
st.markdown("Our goal is to explore the economic implications of natural gas imports and solar power generation in the US. We will analyze the trends in natural gas prices and quantities imported, as well as the growth of solar energy generation over time. This analysis will help us understand the potential benefits of transitioning to renewable energy sources. We will also explore at what point (year) it would make the most sense to impliment Solar Power in the form of Photovoltaic cells, to match the energy consumed.")

st.markdown("There are many Factors that affect the price of natural gas imports including weather, temperature, natural desasters and other events that disrupt supply chains. We will explore these factors in the following sections.")

st.subheader("Natural Gas Import Price (1999 - 2024)")

fig = px.bar(
    allmerged_df,
    x="Date",
    y="Price ($/MCF)",
    color_discrete_sequence=["steelblue"]
)

st.plotly_chart(fig, use_container_width=True)




st.markdown("The price of natural gas has fluctuated over the years, with notable peaks and troughs. This data is crucial for understanding the economic implications of natural gas imports and the potential benefits of transitioning to renewable energy sources. In September 2005, according to the U.S. Energy Information Administration (EIA), the price of natural gas imports was 6.00 per thousand cubic feet (Mcf). This was a significant increase from the previous year, when the price was around 4.00 per Mcf. The increase in price was attributed to several factors, including increased demand for natural gas due to Hurricane Katrina and other weather-related events that disrupted supply chains.")

st.subheader("Temperature (1999 - 2025)")
st.markdown("This chart illustrates the temperature trend in the US from 1990 to 2025.")
fig = px.line(allmerged_df.dropna(subset=["Temperature (F)"]), x="Date", y="Temperature (F)")
# Display in Streamlit
st.plotly_chart(fig)
st.markdown(" The data shows a steady increase in temperature, which is consistent with the global trend of rising temperatures due to climate change. The data also shows seasonal variations, with higher temperatures in the summer months and lower temperatures in the winter months. As temerature decreases the demand for natural gas increases, leading to higher prices. The data shows a clear correlation between temperature and the price of natural gas imports. For example, in January 2014, the average temperature in the US was significantly lower than in previous years, leading to a spike in natural gas prices. This trend is also evident in the winter of 2000/2001, when low temperatures led to increased demand for natural gas and higher prices.")



#print(allmerged_df[["Price ($/MCF)", "Temperature (F)"]].isna().sum())
#print(allmerged_df[["Price ($/MCF)", "Temperature (F)"]].dropna().shape)

#print(allmerged_df[["Price ($/MCF)", "Temperature (F)"]].info())
#print(allmerged_df[["Price ($/MCF)", "Temperature (F)"]].head(10))


corr_df = allmerged_df[["Price ($/MCF)", "Temperature (F)", "Date"]].dropna(subset=["Price ($/MCF)", "Temperature (F)"])

#corr_df["Date"] = pd.to_datetime(corr_df["Date"]).dt.to_period("M").dt.to_timestamp()
#corr_df = corr_df[corr_df["Date"].dt.year > 1998]
print(corr_df.head())

# Compute correlation matrix
correlation = corr_df[["Price ($/MCF)", "Temperature (F)"]].corr()

# Plot the correlation heatmap
st.subheader("Correlation Between Temperature and Natural Gas Price")
fig, ax = plt.subplots(figsize=(4,2))
sns.heatmap(correlation, annot=True, cmap="RdGy" , fmt=".2f", ax=ax)
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

corr_df["Season"] = corr_df["Date"].dt.month.apply(get_season)

# --- Calculate correlations for each season ---
season_correlations = corr_df.groupby("Season")[["Temperature (F)", "Price ($/MCF)"]].corr().iloc[0::2, -1].reset_index()

# Display season correlations
print("Seasonal correlations between temperature and gas price:")
print(season_correlations)

# Visualize as bar chart
fig, ax = plt.subplots(figsize=(3,2))
sns.barplot(data=season_correlations, x="Season", y="Price ($/MCF)", palette="Accent", ax=ax)
ax.set_title("Correlation Between Temperature and Gas Price by Season")
ax.set_ylabel("Correlation Coefficient")
ax.set_ylim(-1, 1)
ax.axhline(0, color='gray', linestyle='--')

# Display in Streamlit
st.pyplot(fig)


st.markdown("The correlation between temperature and natural gas price is significant, with a correlation coefficient of {:.3f}. This indicates that as temperature decreases, the price of natural gas increases. The data also shows a seasonal pattern, with higher prices in the winter months when demand for natural gas is highest.".format(correlation.loc['Temperature (F)', 'Price ($/MCF)']))

st.markdown("The correlation coefficient for each season is as follows:")
for season, corr in zip(season_correlations['Season'], season_correlations['Price ($/MCF)']):
    st.markdown(f"- **{season}:** {corr:.3f}")

st.markdown("The correlation is skewed due to other factors, such as natural disasters and supply chain disruptions, affecting the price of natural gas.")



total_imports = allmerged_df[["Imports (MMcf)", "Price ($/MCF)", "Date"]].copy()
total_imports["Total Import Cost"] = total_imports["Imports (MMcf)"] * ( total_imports["Price ($/MCF)"] * 1000)
total_imports = total_imports.dropna(subset=["Total Import Cost"])

st.subheader("U.S. Natural Gas Imports (1989 - 2024)")
fig = px.line(
    total_imports,
    x="Date",
    y="Imports (MMcf)",
    labels={"U.S. Natural Gas Imports (MMcf)": "Natural Gas Imported (MMcf)"}
)

st.plotly_chart(fig)
st.markdown("The quantity of natural gas imported into the US has fluctuated over the years, with notable peaks and troughs. The data shows a steady increase in the quantity of natural gas imported until 2008, reflecting the growing demand for natural gas in the US. After 2008 the US increased its domestic production of natural gas. The data also shows seasonal variations, with higher imports in the winter months and lower imports in the summer months. This trend is consistent with the seasonal demand for natural gas.")





st.subheader("Natural Gas Production Data (1990 - 2024)")
fig = px.line(allmerged_df[["Production (MMcf)", "Date"]], x="Date", y="Production (MMcf)")
fig.update_layout(yaxis_title="Natural Gas Produced (Million Cublic Feat MMcf)", xaxis_title="Date")
# Display in Streamlit
st.plotly_chart(fig)



corr_df = allmerged_df[["Production (MMcf)", "Imports (MMcf)", "Date"]].dropna(subset=["Production (MMcf)", "Imports (MMcf)"])

print(corr_df.head())

# Compute correlation matrix
correlation = corr_df[["Production (MMcf)", "Imports (MMcf)"]].corr()

# Plot the correlation heatmap
st.subheader("Correlation Matrix: Natural Gas Imports vs Production")
fig, ax = plt.subplots(figsize=(4, 2))
sns.heatmap(correlation, annot=True, cmap="crest", ax=ax)
st.pyplot(fig)

st.markdown(f"The above graphs show a negative correlation of {correlation.iloc[0, 1]:.2f}. This indicates that as the quantity of natural gas imports decreases, the quantity of natural gas produced increases. This trend is consistent with the growing domestic production of natural gas in the US, which has led to a decrease in imports.")



#Total cost to import over the years
st.subheader("Total Natural Gas Import Cost (1989 - 2024)")
fig = px.line(
    total_imports,
    x="Date",
    y="Total Import Cost",
    #title="Total Natural Gas Import Cost (1989 - 2024)",
    labels={"Total Import Cost": "Total Import Cost (USD)"}
)

# Display in Streamlit
st.plotly_chart(fig)

st.markdown("By multiplying the price of natural gas by the quantity imported, we can see the total cost to import natural gas. The price of natural gas is listed in the dataset as per thousand cubic feet ($/Mcf), and the quantity dataset displays the values int the unit of million cubic feet (MMcf). To normalize these values, we multiply the quantity by 1000 then multiply the result by the cost to get the total cost incurred by the US for importing natural gas.")





merged_df4 = allmerged_df[["Date",  "Imports (MMcf)", "Price ($/MCF)"]].copy()
# Create Month Name and Number for ordering
merged_df4["Month Name"] = merged_df4["Date"].dt.strftime('%B')
merged_df4["Month Number"] = merged_df4["Date"].dt.month

# Sort for correct month order
merged_df4 = merged_df4.sort_values("Month Number")

# Define order explicitly
month_order = pd.date_range("2000-01-01", periods=12, freq="M").strftime("%B")


# Create boxplots
fig, axes = plt.subplots(2, 1, figsize=(12, 16), sharex=False)

# 1. Imports
sns.boxplot(
    data=merged_df4,
    x="Month Name",
    y="Imports (MMcf)",
    order=month_order,
    ax=axes[0],
    palette="crest",
    width=0.5
)
axes[0].set_title("Seasonal Distribution of Natural Gas Imports")

#====SPLIT INTO TWO PAGES NOT TWO PLOTS ON THE SAME PAGE=====

# 3. Prices
sns.boxplot(
    data=merged_df4,
    x="Month Name",
    y="Price ($/MCF)",
    order=month_order,
    ax=axes[1],
    palette="BuPu",
    width=0.5
)
axes[1].set_title("Seasonal Distribution of Natural Gas Import Prices")
axes[1].set_xlabel("Month")

plt.xticks(ticks=range(0, 12), labels=[
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
], fontsize=10)

# Rotate x-axis labels for clarity


for ax in axes:
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_xlabel("-------------------------------------------------------------------------------------------------------------------------------------------- Month --------------------------------------------------------------------------------------------------------------------------------------------")
    ax.grid(axis='y', linestyle='--', alpha=0.5)

# Display the plot
plt.tight_layout(pad=2.5)
st.pyplot(fig)






#KEY HIGHLIGHTS

# 1. Highest Monthly Import
max_import_row = allmerged_df.loc[allmerged_df["Imports (MMcf)"].idxmax()]
max_import_value = max_import_row["Imports (MMcf)"]
max_import_date = max_import_row["Date"].strftime("%b %Y")

# 2. Year with Highest Production
yearly_production = allmerged_df.groupby("Date")["Production (MMcf)"].sum()
highest_production_year = yearly_production.idxmax()
highest_production_value = yearly_production.max()

# 3. Month with Highest Cost
max_cost_row = total_imports.loc[total_imports["Total Import Cost"].idxmax()]
max_cost_value = max_cost_row["Total Import Cost"]
max_cost_date = max_cost_row["Date"].strftime("%b %Y")




# Display metrics
st.subheader("📊 Key Highlights")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📈 Highest Monthly Import", value=f"{max_import_value:,.0f} MMcf", delta=max_import_date)

with col2:
    st.metric(label="🏭 Highest Production Year", value=f"{highest_production_year.year}", delta=f"{highest_production_value:,.0f} units")

with col3:
    st.metric(label="💰 Highest Monthly Import Cost", value=f"${max_cost_value:,.0f}", delta=max_cost_date)





