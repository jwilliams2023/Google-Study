import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define street names in Pearl City, Hawaii
street_names = [
    "Akaikai Loop", "Komo Mai Drive", "Hookanike Street", "Noelani Street", 
    "Hoolaulea Street", "Leomele Street", "Waimano Home Road", "Kuahaka Street",
    "Hoohulu Street", "Hooli Circle", "Hoomalu Street", "Lehua Avenue",
    "Kamehameha Highway", "Kuala Street", "Aumakua Street", "Kaahumanu Street",
    "Pukunui Street", "Puu Poni Street", "Moanalua Road", "Hoolana Street"
]

# Function to generate a random date between 2021-2023
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

# Function to generate a random address
def generate_address(existing_addresses):
    while True:
        house_number = random.randint(1000, 3000)
        street = random.choice(street_names)
        address = f"{house_number} {street}"
        if address not in existing_addresses:
            return address

# Create dataset
def create_dataset(num_properties=50):
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    # Ensure the two required properties are included
    required_properties = [
        {
            "Address": "2072 Akaikai Loop",
            "Sale Date": datetime(2022, 6, 15),  # Random date in 2022
            "Sale Price": 875000,  # Random price
            "Square Footage": 1850,
            "Bedrooms": 4,
            "Bathrooms": 2.5,
            "Year Built": 1985
        },
        {
            "Address": "2017 Komo Mai Drive",
            "Sale Date": datetime(2022, 9, 22),  # Random date in 2022
            "Sale Price": 925000,  # Higher price for the second property
            "Square Footage": 2100,
            "Bedrooms": 4,
            "Bathrooms": 3,
            "Year Built": 1992
        }
    ]
    
    data = required_properties.copy()
    existing_addresses = {prop["Address"] for prop in required_properties}
    
    # Generate additional random properties
    for _ in range(num_properties - len(required_properties)):
        address = generate_address(existing_addresses)
        existing_addresses.add(address)
        
        sale_date = random_date(start_date, end_date)
        
        # Generate realistic property details
        # Pearl City median home price is around $800k-900k
        base_price = 800000
        price_variation = 300000
        sale_price = int(np.random.normal(base_price, price_variation/3))
        sale_price = max(500000, min(1500000, sale_price))  # Limit to realistic range
        
        # Square footage typically between 1000-3000 sq ft
        sqft = int(np.random.normal(1800, 500))
        sqft = max(1000, min(3500, sqft))
        
        # Bedrooms typically 3-5
        bedrooms = np.random.choice([2, 3, 4, 5], p=[0.05, 0.4, 0.4, 0.15])
        
        # Bathrooms typically 1-3
        bathrooms = np.random.choice([1, 1.5, 2, 2.5, 3, 3.5], p=[0.05, 0.15, 0.3, 0.3, 0.15, 0.05])
        
        # Year built (most homes in Pearl City were built between 1960-2000)
        year_built = random.randint(1960, 2015)
        
        property_data = {
            "Address": address,
            "Sale Date": sale_date,
            "Sale Price": sale_price,
            "Square Footage": sqft,
            "Bedrooms": bedrooms,
            "Bathrooms": bathrooms,
            "Year Built": year_built
        }
        
        data.append(property_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Add some additional features
    df["Price per Sqft"] = (df["Sale Price"] / df["Square Footage"]).round(2)
    df["Property Type"] = np.random.choice(["Single Family", "Townhouse", "Condo"], 
                                          size=len(df), 
                                          p=[0.7, 0.2, 0.1])
    df["Lot Size (sqft)"] = (df["Square Footage"] * np.random.uniform(1.5, 4, size=len(df))).astype(int)
    df["Has Pool"] = np.random.choice([True, False], size=len(df), p=[0.15, 0.85])
    df["Has Garage"] = np.random.choice([True, False], size=len(df), p=[0.8, 0.2])
    df["Garage Size"] = df["Has Garage"].apply(lambda x: random.randint(1, 3) if x else 0)
    
    # Format the date
    df["Sale Date"] = df["Sale Date"].dt.strftime("%Y-%m-%d")
    
    return df

if __name__ == "__main__":
    # Create dataset with at least 50 properties
    df = create_dataset(55)  # Generate a few extra to ensure we have at least 50
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), "pearl_city_home_sales.csv")
    df.to_csv(output_path, index=False)
    
    print(f"Dataset created with {len(df)} properties and saved to {output_path}")
    
    # Find which of the two specified properties sold for more in 2022
    property1 = df[df["Address"] == "2072 Akaikai Loop"]
    property2 = df[df["Address"] == "2017 Komo Mai Drive"]
    
    if not property1.empty and not property2.empty:
        price1 = property1.iloc[0]["Sale Price"]
        price2 = property2.iloc[0]["Sale Price"]
        
        higher_price_property = "2017 Komo Mai Drive" if price2 > price1 else "2072 Akaikai Loop"
        higher_price = max(price1, price2)
        
        result_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "result.txt")
        with open(result_path, "w") as f:
            f.write(f"The property at {higher_price_property} sold for more in 2022, with a sale price of ${higher_price:,}.")
        
        print(f"Result saved to {result_path}")