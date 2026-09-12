import pandas as pd

# Load one CSV with 3 contract columns
df_CO = pd.read_csv('data/raw/Brent(CO).csv')
# df has columns: Date, CL1_Price, CL2_Price, CL3_Price

# Python easily unpivots or filters to single contract if needed
CO1 = df_CO[['Date', 'CO1']]
CO2 = df_CO[['Date', 'CO2']]
CO3 = df_CO[['Date', 'CO3']]


print(CO1.head())