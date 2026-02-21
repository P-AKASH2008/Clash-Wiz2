import pandas as pd

df = pd.read_csv("../ml_core/data/processed/final_dataset.csv")

# Example: win rate when Card A present and Card B present
card_columns = [col for col in df.columns if col.startswith("card_")]

matrix = []

for card1 in card_columns:
    for card2 in card_columns:
        subset = df[(df[card1] == 1) & (df[card2] == 1)]
        if len(subset) > 30:  # minimum matches filter
            win_rate = subset["winner"].mean()
            matrix.append([card1, card2, win_rate])

matrix_df = pd.DataFrame(matrix, columns=["card_A", "card_B", "win_rate"])
matrix_df.to_csv("matchup_matrix.csv", index=False)

print(matrix_df.head())