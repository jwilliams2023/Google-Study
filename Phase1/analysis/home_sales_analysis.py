import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Set style for plots
plt.style.use('ggplot')
sns.set_palette("Set2")

# Load the dataset
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "pearl_city_home_sales.csv")
df = pd.read_csv(data_path)

# Convert Sale Date to datetime
df['Sale Date'] = pd.to_datetime(df['Sale Date'])
df['Month'] = df['Sale Date'].dt.month
df['Year'] = df['Sale Date'].dt.year
df['Quarter'] = df['Sale Date'].dt.quarter

# Create output directory for plots
output_dir = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(output_dir, exist_ok=True)

# 1. Current estimated value of a typical home in the area
print("\n1. CURRENT ESTIMATED VALUE OF A TYPICAL HOME IN PEARL CITY")
print("=" * 60)

# Calculate basic statistics
mean_price = df['Sale Price'].mean()
median_price = df['Sale Price'].median()
mean_price_per_sqft = df['Price per Sqft'].mean()

print(f"Mean Sale Price: ${mean_price:,.2f}")
print(f"Median Sale Price: ${median_price:,.2f}")
print(f"Mean Price per Square Foot: ${mean_price_per_sqft:.2f}")

# Calculate price trends over time
yearly_prices = df.groupby('Year')['Sale Price'].agg(['mean', 'median', 'count'])
print("\nYearly Price Trends:")
print(yearly_prices)

# Calculate price appreciation rate
if len(yearly_prices) > 1:
    first_year = yearly_prices.index.min()
    last_year = yearly_prices.index.max()
    price_appreciation = (yearly_prices.loc[last_year, 'mean'] / yearly_prices.loc[first_year, 'mean'] - 1) * 100
    annual_appreciation = price_appreciation / (last_year - first_year)
    print(f"\nAnnual Price Appreciation Rate: {annual_appreciation:.2f}%")

# Estimate current value based on the latest data and appreciation rate
current_year = 2025  # Current year
years_since_last_data = current_year - last_year
estimated_current_value = median_price * (1 + annual_appreciation/100) ** years_since_last_data

print(f"\nEstimated Current Value of a Typical Home (as of {current_year}): ${estimated_current_value:,.2f}")

# Plot price distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Sale Price'], kde=True, bins=15)
plt.title('Distribution of Home Sale Prices in Pearl City (2021-2023)')
plt.xlabel('Sale Price ($)')
plt.ylabel('Frequency')
plt.ticklabel_format(style='plain', axis='x')
plt.savefig(os.path.join(output_dir, 'price_distribution.png'))

# Plot price trends over time
plt.figure(figsize=(12, 6))
df.groupby([df['Sale Date'].dt.year, df['Sale Date'].dt.month])['Sale Price'].mean().plot()
plt.title('Average Home Sale Price Trend (2021-2023)')
plt.xlabel('Year-Month')
plt.ylabel('Average Sale Price ($)')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'price_trend.png'))

# 2. Best time to sell based on seasonal trends
print("\n\n2. BEST TIME TO SELL BASED ON SEASONAL TRENDS")
print("=" * 60)

# Analyze sales by month
monthly_sales = df.groupby('Month').agg({
    'Sale Price': ['mean', 'median', 'count'],
    'Price per Sqft': 'mean'
})

print("Monthly Sales Analysis:")
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_sales.index = month_names[:len(monthly_sales)]
print(monthly_sales)

# Find the month with highest average price
best_price_month = monthly_sales['Sale Price']['mean'].idxmax()
best_price_month_value = monthly_sales['Sale Price']['mean'].max()

# Find the month with highest number of sales
best_volume_month = monthly_sales['Sale Price']['count'].idxmax()
best_volume_month_value = monthly_sales['Sale Price']['count'].max()

print(f"\nMonth with Highest Average Price: {best_price_month} (${best_price_month_value:,.2f})")
print(f"Month with Highest Sales Volume: {best_volume_month} ({best_volume_month_value} sales)")

# Plot monthly price trends
plt.figure(figsize=(12, 6))
monthly_sales['Sale Price']['mean'].plot(kind='bar', color='skyblue')
plt.title('Average Sale Price by Month')
plt.xlabel('Month')
plt.ylabel('Average Sale Price ($)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'monthly_price_trends.png'))

# Plot monthly sales volume
plt.figure(figsize=(12, 6))
monthly_sales['Sale Price']['count'].plot(kind='bar', color='lightgreen')
plt.title('Number of Home Sales by Month')
plt.xlabel('Month')
plt.ylabel('Number of Sales')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'monthly_sales_volume.png'))

# Analyze by quarter
quarterly_sales = df.groupby('Quarter').agg({
    'Sale Price': ['mean', 'median', 'count'],
    'Price per Sqft': 'mean'
})

print("\nQuarterly Sales Analysis:")
quarterly_sales.index = ['Q1', 'Q2', 'Q3', 'Q4'][:len(quarterly_sales)]
print(quarterly_sales)

# Find the quarter with highest average price
best_price_quarter = quarterly_sales['Sale Price']['mean'].idxmax()
best_price_quarter_value = quarterly_sales['Sale Price']['mean'].max()

print(f"\nQuarter with Highest Average Price: {best_price_quarter} (${best_price_quarter_value:,.2f})")

# 3. Which home improvements might yield the best return on investment
print("\n\n3. HOME IMPROVEMENTS WITH BEST RETURN ON INVESTMENT")
print("=" * 60)

# Analyze price differences based on features
print("Impact of Different Features on Home Price:")

# Impact of number of bedrooms
bedroom_analysis = df.groupby('Bedrooms').agg({
    'Sale Price': ['mean', 'median', 'count'],
    'Price per Sqft': 'mean',
    'Square Footage': 'mean'
}).sort_index()

print("\nImpact of Number of Bedrooms:")
print(bedroom_analysis)

# Impact of number of bathrooms
bathroom_analysis = df.groupby('Bathrooms').agg({
    'Sale Price': ['mean', 'median', 'count'],
    'Price per Sqft': 'mean',
    'Square Footage': 'mean'
}).sort_index()

print("\nImpact of Number of Bathrooms:")
print(bathroom_analysis)

# Impact of having a pool
pool_analysis = df.groupby('Has Pool').agg({
    'Sale Price': ['mean', 'median', 'count'],
    'Price per Sqft': 'mean',
    'Square Footage': 'mean'
})

print("\nImpact of Having a Pool:")
print(pool_analysis)

# Calculate the premium for having a pool
if len(pool_analysis) > 1:
    pool_premium = pool_analysis['Sale Price']['mean'][True] - pool_analysis['Sale Price']['mean'][False]
    pool_premium_percentage = (pool_premium / pool_analysis['Sale Price']['mean'][False]) * 100
    print(f"Pool Premium: ${pool_premium:,.2f} ({pool_premium_percentage:.2f}%)")

# Impact of having a garage
garage_analysis = df.groupby('Has Garage').agg({
    'Sale Price': ['mean', 'median', 'count'],
    'Price per Sqft': 'mean',
    'Square Footage': 'mean'
})

print("\nImpact of Having a Garage:")
print(garage_analysis)

# Calculate the premium for having a garage
if len(garage_analysis) > 1:
    garage_premium = garage_analysis['Sale Price']['mean'][True] - garage_analysis['Sale Price']['mean'][False]
    garage_premium_percentage = (garage_premium / garage_analysis['Sale Price']['mean'][False]) * 100
    print(f"Garage Premium: ${garage_premium:,.2f} ({garage_premium_percentage:.2f}%)")

# Impact of garage size
garage_size_analysis = df.groupby('Garage Size').agg({
    'Sale Price': ['mean', 'median', 'count'],
    'Price per Sqft': 'mean',
    'Square Footage': 'mean'
}).sort_index()

print("\nImpact of Garage Size:")
print(garage_size_analysis)

# Impact of property type
property_type_analysis = df.groupby('Property Type').agg({
    'Sale Price': ['mean', 'median', 'count'],
    'Price per Sqft': 'mean',
    'Square Footage': 'mean'
})

print("\nImpact of Property Type:")
print(property_type_analysis)

# Plot impact of bedrooms on price
plt.figure(figsize=(10, 6))
sns.barplot(x=df['Bedrooms'].astype(str), y=df['Sale Price'])
plt.title('Impact of Number of Bedrooms on Sale Price')
plt.xlabel('Number of Bedrooms')
plt.ylabel('Average Sale Price ($)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'bedroom_impact.png'))

# Plot impact of bathrooms on price
plt.figure(figsize=(10, 6))
sns.barplot(x=df['Bathrooms'].astype(str), y=df['Sale Price'])
plt.title('Impact of Number of Bathrooms on Sale Price')
plt.xlabel('Number of Bathrooms')
plt.ylabel('Average Sale Price ($)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'bathroom_impact.png'))

# Plot impact of having a pool
plt.figure(figsize=(8, 6))
sns.barplot(x=df['Has Pool'].astype(str), y=df['Sale Price'])
plt.title('Impact of Having a Pool on Sale Price')
plt.xlabel('Has Pool')
plt.ylabel('Average Sale Price ($)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'pool_impact.png'))

# Plot impact of having a garage
plt.figure(figsize=(8, 6))
sns.barplot(x=df['Has Garage'].astype(str), y=df['Sale Price'])
plt.title('Impact of Having a Garage on Sale Price')
plt.xlabel('Has Garage')
plt.ylabel('Average Sale Price ($)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'garage_impact.png'))

# Calculate ROI for different improvements
print("\nEstimated ROI for Different Home Improvements:")

# Typical costs of improvements (estimated)
improvement_costs = {
    "Add Bedroom": 50000,
    "Add Bathroom": 30000,
    "Add Pool": 60000,
    "Add Garage (1-car)": 25000,
    "Add Garage (2-car)": 40000,
    "Upgrade to Single Family": 100000  # If converting from condo/townhouse
}

# Calculate ROI for adding a bedroom
if len(bedroom_analysis) > 1:
    # Find the most common bedroom count
    most_common_bedroom = df['Bedrooms'].mode()[0]
    if most_common_bedroom < max(df['Bedrooms']):
        bedroom_premium = bedroom_analysis['Sale Price']['mean'][most_common_bedroom + 1] - bedroom_analysis['Sale Price']['mean'][most_common_bedroom]
        bedroom_roi = (bedroom_premium / improvement_costs["Add Bedroom"]) * 100
        print(f"ROI for Adding a Bedroom (from {most_common_bedroom} to {most_common_bedroom + 1}): {bedroom_roi:.2f}%")

# Calculate ROI for adding a bathroom
if len(bathroom_analysis) > 1:
    # Find the most common bathroom count
    most_common_bathroom = df['Bathrooms'].mode()[0]
    next_bathroom = sorted(df['Bathrooms'].unique())[list(sorted(df['Bathrooms'].unique())).index(most_common_bathroom) + 1] if list(sorted(df['Bathrooms'].unique())).index(most_common_bathroom) < len(df['Bathrooms'].unique()) - 1 else most_common_bathroom
    if most_common_bathroom < max(df['Bathrooms']):
        bathroom_premium = bathroom_analysis['Sale Price']['mean'][next_bathroom] - bathroom_analysis['Sale Price']['mean'][most_common_bathroom]
        bathroom_roi = (bathroom_premium / improvement_costs["Add Bathroom"]) * 100
        print(f"ROI for Adding a Bathroom (from {most_common_bathroom} to {next_bathroom}): {bathroom_roi:.2f}%")

# Calculate ROI for adding a pool
if len(pool_analysis) > 1:
    pool_roi = (pool_premium / improvement_costs["Add Pool"]) * 100
    print(f"ROI for Adding a Pool: {pool_roi:.2f}%")

# Calculate ROI for adding a garage
if len(garage_analysis) > 1:
    garage_roi = (garage_premium / improvement_costs["Add Garage (1-car)"]) * 100
    print(f"ROI for Adding a 1-car Garage: {garage_roi:.2f}%")

# Calculate ROI for upgrading garage size
if 1 in garage_size_analysis.index and 2 in garage_size_analysis.index:
    garage_upgrade_premium = garage_size_analysis['Sale Price']['mean'][2] - garage_size_analysis['Sale Price']['mean'][1]
    garage_upgrade_cost = improvement_costs["Add Garage (2-car)"] - improvement_costs["Add Garage (1-car)"]
    garage_upgrade_roi = (garage_upgrade_premium / garage_upgrade_cost) * 100
    print(f"ROI for Upgrading from 1-car to 2-car Garage: {garage_upgrade_roi:.2f}%")

# Calculate ROI for property type upgrade if applicable
if 'Condo' in property_type_analysis.index and 'Single Family' in property_type_analysis.index:
    property_upgrade_premium = property_type_analysis['Sale Price']['mean']['Single Family'] - property_type_analysis['Sale Price']['mean']['Condo']
    property_upgrade_roi = (property_upgrade_premium / improvement_costs["Upgrade to Single Family"]) * 100
    print(f"ROI for Upgrading from Condo to Single Family: {property_upgrade_roi:.2f}%")

# Summary of findings
print("\nSUMMARY OF FINDINGS")
print("=" * 60)
print(f"1. Current Estimated Value: ${estimated_current_value:,.2f}")
print(f"2. Best Time to Sell: {best_price_month} (highest price) or {best_volume_month} (highest volume)")

# Determine best ROI improvements
roi_values = {}
if 'bedroom_roi' in locals():
    roi_values["Adding a Bedroom"] = bedroom_roi
if 'bathroom_roi' in locals():
    roi_values["Adding a Bathroom"] = bathroom_roi
if 'pool_roi' in locals():
    roi_values["Adding a Pool"] = pool_roi
if 'garage_roi' in locals():
    roi_values["Adding a Garage"] = garage_roi
if 'garage_upgrade_roi' in locals():
    roi_values["Upgrading Garage"] = garage_upgrade_roi
if 'property_upgrade_roi' in locals():
    roi_values["Upgrading Property Type"] = property_upgrade_roi

if roi_values:
    best_improvement = max(roi_values, key=roi_values.get)
    print(f"3. Best Home Improvement for ROI: {best_improvement} ({roi_values[best_improvement]:.2f}%)")
else:
    print("3. Insufficient data to determine best home improvement for ROI")

print("\nAnalysis complete. Plots saved to:", output_dir)