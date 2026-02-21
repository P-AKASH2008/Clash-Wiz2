import pandas as pd

df = pd.read_csv("../ml_core/data/processed/final_dataset.csv")

card_columns = [col for col in df.columns if col.startswith("card_")]

usage = {}

for card in card_columns:
    usage[card] = df[card].sum()

usage_df = pd.DataFrame(usage.items(), columns=["card", "usage"])
usage_df = usage_df.sort_values(by="usage", ascending=False)

usage_df.to_csv("card_usage.csv", index=False)

print(usage_df.head())
