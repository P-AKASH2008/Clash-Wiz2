import pandas as pd
import json

# load dataset
df = pd.read_pickle("../data/raw/clash_matches.pkl")

# load metadata
with open("../../config/card_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# get all unique card IDs
card_ids = set()

for deck in df["deckA"]:
    for card in deck:
        card_ids.add(card)

for deck in df["deckB"]:
    for card in deck:
        card_ids.add(card)

card_ids = sorted(list(card_ids))

print("Total unique cards:", len(card_ids))
print(card_ids[:20])  # preview