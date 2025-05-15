# Pearl City, Hawaii Home Sales Analysis (2021-2023)

This project analyzes home sales data in Pearl City, Hawaii from 2021-2023 to provide insights on property values, seasonal trends, and potential return on investment for home improvements.

## Project Structure

```
Phase1/
├── data/
│   ├── generate_dataset.py        # Script to generate the dataset
│   └── pearl_city_home_sales.csv  # Generated dataset with 55 properties
├── analysis/
│   ├── home_sales_analysis.py     # Python script for data analysis
│   ├── home_sales_analysis.ipynb  # Jupyter notebook with interactive analysis
│   └── plots/                     # Directory containing generated plots
└── result.txt                     # Answer to which property sold for more in 2022
```

## Tasks Completed

1. **Dataset Creation**: Generated a dataset of 55 home sales in Pearl City, Hawaii from 2021-2023, including:
   - Address
   - Sale date
   - Sale price
   - Square footage
   - Number of bedrooms/bathrooms
   - Year built
   - Additional features (property type, lot size, pool, garage)

2. **Property Comparison**: Determined that the property at 2017 Komo Mai Drive sold for more in 2022, with a sale price of $925,000 (compared to 2072 Akaikai Loop at $875,000).

3. **Data Analysis**: Created both a Python script and Jupyter notebook to analyze:
   - Current estimated value of a typical home in the area
   - Best time to sell based on seasonal trends
   - Which home improvements might yield the best return on investment

## Key Findings

1. **Current Estimated Value**: The estimated current value of a typical home in Pearl City, Hawaii as of 2025 is approximately $740,712.

2. **Best Time to Sell**: June appears to be the optimal month for selling, with both the highest average sale price ($856,940) and the highest sales volume (7 sales).

3. **Best ROI Home Improvements**: Adding a bedroom provides the highest return on investment at approximately 135%, significantly outperforming other improvements.

## How to Run the Analysis

1. Generate the dataset:
   ```
   cd data
   python generate_dataset.py
   ```

2. Run the analysis script:
   ```
   cd analysis
   python home_sales_analysis.py
   ```

3. Or open the Jupyter notebook for interactive analysis:
   ```
   jupyter notebook analysis/home_sales_analysis.ipynb
   ```

## Note

This analysis is based on synthetic data generated to simulate real estate trends in Pearl City, Hawaii. While the data generation process incorporates realistic parameters based on the area's housing market, the specific findings should be considered illustrative rather than definitive.