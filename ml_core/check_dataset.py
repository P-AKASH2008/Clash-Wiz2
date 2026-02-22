import pandas as pd
df = pd.read_pickle("data/raw/clash_dataset.pkl")
print(df.head())
print(len(df))