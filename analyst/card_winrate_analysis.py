import pandas as pd

df = pd.read_csv("../ml_core/data/processed/final_dataset.csv")

# Extract all card columns (binary encoded)
card_columns = [col for col in df.columns if col.startswith("card_")]

win_rates = {}

for card in card_columns:
    total_usage = df[card].sum()
    wins = df[df["winner"] == 1][card].sum()

    if total_usage > 0:
        win_rate = wins / total_usage
        win_rates[card] = win_rate

# Convert to dataframe
winrate_df = pd.DataFrame(win_rates.items(), columns=["card", "win_rate"])
winrate_df = winrate_df.sort_values(by="win_rate", ascending=False)

winrate_df.to_csv("card_winrates.csv", index=False)

print(winrate_df.head())