import pandas as pd

u = pd.read_csv("config/universe.csv")
print(u.shape)

print(u.sector.value_counts())
print(repr(u.loc[u.root=="C","gen1"].item( )))

