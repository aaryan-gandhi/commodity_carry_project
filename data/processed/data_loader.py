import pandas as pd

# Load one CSV with 3 contract columns
df_CO = pd.read_csv('data/raw/Brent(CO).csv')

# Brent Oil
CO1 = df_CO[['Date', 'CO1']]
CO2 = df_CO[['Date', 'CO2']]
CO3 = df_CO[['Date', 'CO3']]

# Coffee
df_KC = pd.read_csv('data/raw/Coffee(KC).csv')

KC1 = df_KC[['Date', 'KC1']]
KC2 = df_KC[['Date', 'KC2']]
KC3 = df_KC[['Date', 'KC3']]

# Copper
df_HG = pd.read_csv('data/raw/Copper.csv')

HG1 = df_HG[['Date', 'HG1']]
HG2 = df_HG[['Date', 'HG2']]
HG3 = df_HG[['Date', 'HG3']]

# Corn
df_C = pd.read_csv('data/raw/Corn(C).csv')

C1 = df_C[['Date', 'C1']]
C2 = df_C[['Date', 'C2']]
C3 = df_C[['Date', 'C3']]

# Crude Oil
df_CL = pd.read_csv('data/raw/Crudeoil.csv')

CL1 = df_CL[['Date', 'CL1']]
CL2 = df_CL[['Date', 'Cl2']]
CL3 = df_CL[['Date', 'CL3']]

# Gold
df_GC = pd.read_csv('data/raw/Gold.csv')

GC1 = df_GC[['Date', 'GC1']]
GC2 = df_GC[['Date', 'GC2']]
GC3 = df_GC[['Date', 'GC3']]

# Heating Oil
df_HO = pd.read_csv('data/raw/Heatingoil(HO).csv')

HO1 = df_HO[['Date', 'HO1']]
HO2 = df_HO[['Date', 'HO2']]
HO3 = df_HO[['Date', 'HO3']]

# Natural Gas
df_NG = pd.read_csv('data/raw/Naturalgas.csv')

NG1 = df_NG[['Date', 'NG1']]
NG2 = df_NG[['Date', 'NG2']]
NG3 = df_NG[['Date', 'NG3']]

# Silver
df_SI = pd.read_csv('data/raw/Silver(SI).csv')

SI1 = df_SI[['Date', 'SI1']]
SI2 = df_SI[['Date', 'SI2']]
SI3 = df_SI[['Date', 'SI3']]

# Soybeans
df_S = pd.read_csv('data/raw/Soybeans(S).csv')

S1 = df_S[['Date', 'S1']]
S2 = df_S[['Date', 'S2']]
S3 = df_S[['Date', 'S3']]

# Sugar
df_SB = pd.read_csv('data/raw/Sugar(SB).csv')

SB1 = df_SB[['Date', 'SB1']]
SB2 = df_SB[['Date', 'SB2']]
SB3 = df_SB[['Date', 'SB3']]

# Wheat
df_W = pd.read_csv('data/raw/Wheat(W).csv')

W1 = df_W[['Date', 'W1']]
W2 = df_W[['Date', 'W2']]
W3 = df_W[['Date', 'W3']]