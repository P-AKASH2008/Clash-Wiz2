import pandas as pd

# load pickle dataset
df = pd.read_pickle("data/raw/clash_matches.pkl")

print("\nDATASET TYPE:")
print(type(df))

print("\nDATASET SHAPE:")
print(df.shape)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:")
print(df.head())

print("\nMISSING VALUES:")
print(df.isnull().sum())