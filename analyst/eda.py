import pandas as pd

# Load RAW dataset for now
df = pd.read_pickle("../ml_core/data/raw/clash_matches.pkl")

print("Shape:", df.shape)
print("\nColumns:\n", df.columns)
print("\nMissing values:\n", df.isnull().sum())
print("\nFirst 5 rows:\n", df.head())