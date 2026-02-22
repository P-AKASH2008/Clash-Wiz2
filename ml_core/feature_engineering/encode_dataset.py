import pandas as pd
import json
from pathlib import Path

print("Loading raw dataset...")

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_PATH = BASE_DIR / "data/raw/clash_dataset.pkl"
OUT_PATH = BASE_DIR / "data/processed/final_dataset.csv"
META_PATH = BASE_DIR / "data/card_metadata.json"

df = pd.read_pickle(RAW_PATH)

# ------------------ load metadata ------------------
with open(META_PATH, "r", encoding="utf-8") as f:
    CARD_META = json.load(f)

print("Loaded metadata for", len(CARD_META), "cards")

# ------------------ deck feature extractor ------------------
def extract_deck_features(deck):
    total_elixir = 0
    count = 0

    types = {"troop":0, "spell":0, "building":0}

    for cid in deck:
        cid = str(cid)

        if cid not in CARD_META:
            continue

        info = CARD_META[cid]

        # elixir
        if "elixir" in info:
            total_elixir += info["elixir"]
            count += 1

        # type
        if "type" in info:
            t = info["type"].lower()
            if t in types:
                types[t] += 1

    avg_elixir = total_elixir / count if count else 0
    return avg_elixir, types

# ------------------ encoding ------------------
rows = []

for _, match in df.iterrows():

    deckA = match["deckA"]
    deckB = match["deckB"]

    row = {}

    # One‑hot encode cards
    for cid in deckA:
        row[f"A_{cid}"] = 1
    for cid in deckB:
        row[f"B_{cid}"] = 1

    # Fill missing card columns later
    # ----- Deck A features -----
    avgA, typesA = extract_deck_features(deckA)
    row["A_avg_elixir"] = avgA
    row["A_troops"] = typesA["troop"]
    row["A_spells"] = typesA["spell"]
    row["A_buildings"] = typesA["building"]

    # ----- Deck B features -----
    avgB, typesB = extract_deck_features(deckB)
    row["B_avg_elixir"] = avgB
    row["B_troops"] = typesB["troop"]
    row["B_spells"] = typesB["spell"]
    row["B_buildings"] = typesB["building"]

    # gamemode (safe feature)
    row["gamemode"] = match["gamemode"]

    # label
    row["winner"] = match["label"]

    rows.append(row)

print("Building dataframe...")
final_df = pd.DataFrame(rows).fillna(0)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
final_df.to_csv(OUT_PATH, index=False)

print("Saved encoded dataset →", OUT_PATH)