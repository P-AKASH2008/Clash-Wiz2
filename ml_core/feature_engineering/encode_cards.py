import pandas as pd
from tqdm import tqdm

print("Loading dataset...")
df = pd.read_pickle("../data/raw/clash_matches.pkl")
df = df.sample(200000, random_state=42)

# ---- Step 1: get all unique cards ----
all_cards = set()

for deck in df["deckA"]:
    all_cards.update(deck)

for deck in df["deckB"]:
    all_cards.update(deck)

all_cards = sorted(list(all_cards))

# map each card id to index
card_to_index = {card:i for i,card in enumerate(all_cards)}

print("Total cards:", len(card_to_index))

# ---- Step 2: encoding function ----
def encode_deck(deck):
    vector = [0]*len(card_to_index)
    for card in deck:
        vector[card_to_index[card]] = 1
    return vector

# ---- Step 3: build dataset ----
features = []
labels = []

print("Encoding matches...")

for _, row in tqdm(df.iterrows(), total=len(df)):
    deckA_vec = encode_deck(row["deckA"])
    deckB_vec = encode_deck(row["deckB"])

    match_vector = deckA_vec + deckB_vec

    features.append(match_vector)
    labels.append(row["label"])

# ---- Step 4: save dataset ----
X = pd.DataFrame(features)
X["winner"] = labels

print("Saving processed dataset...")
X.to_csv("../data/processed/final_dataset.csv", index=False)

print("DONE ✅")