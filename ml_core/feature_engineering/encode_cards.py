import pandas as pd
import csv
from tqdm import tqdm
from elixir_values import deck_elixir
from role_features import deck_type_counts

print("Loading dataset...")
df = pd.read_pickle("../data/raw/clash_matches.pkl")

SAMPLE_SIZE = 1000000
df = df.sample(SAMPLE_SIZE, random_state=42)

# -------- REMOVE MIRROR MATCHES (VERY IMPORTANT) --------
print("Removing mirror matches...")
df = df[df["deckA"] != df["deckB"]]
print("Remaining matches:", len(df))

# ---------------------------------------------------
# STEP 1: Build global card index (VERY IMPORTANT)
# ---------------------------------------------------
print("Building card index...")

all_cards = set()

for deck in df["deckA"]:
    all_cards.update(deck)

for deck in df["deckB"]:
    all_cards.update(deck)

all_cards = sorted(list(all_cards))
card_to_index = {card: i for i, card in enumerate(all_cards)}

print("Total cards:", len(card_to_index))

# Save mapping (backend will reuse this later!)
pd.Series(card_to_index).to_json("../data/processed/card_index.json")

# ---------------------------------------------------
# STEP 2: Deck encoder
# ---------------------------------------------------
def encode_deck(deck):
    vec = [0] * len(card_to_index)
    for c in deck:
        idx = card_to_index.get(c)
        if idx is not None:
            vec[idx] = 1
    return vec

# ---------------------------------------------------
# STEP 3: STREAM WRITE CSV (KEY IMPROVEMENT)
# ---------------------------------------------------
output_path = "../data/processed/final_dataset.csv"

print("Encoding & writing dataset...")

with open(output_path, "w", newline="") as f:
    writer = csv.writer(f)

    # header
    header = [f"f{i}" for i in range(len(card_to_index)*2 + 9)]
    header.append("winner")
    writer.writerow(header)
    
    for _, row in tqdm(df.iterrows(), total=len(df)):

        deckA = row["deckA"]
        deckB = row["deckB"]

        deckA_vec = encode_deck(deckA)
        deckB_vec = encode_deck(deckB)

        # ---- elixir features ----
        elixirA = deck_elixir(deckA)
        elixirB = deck_elixir(deckB)

        # ---- role features ----
        tA, sA, bA = deck_type_counts(deckA)
        tB, sB, bB = deck_type_counts(deckB)

        match_vector = (
            deckA_vec +
            deckB_vec +
            [
                elixirA, elixirB, elixirA - elixirB,
                tA, sA, bA,
                tB, sB, bB,
                tA - tB, sA - sB, bA - bB
            ]
        )

        writer.writerow(match_vector + [row["label"]])

print("DONE ✅ Dataset created successfully")