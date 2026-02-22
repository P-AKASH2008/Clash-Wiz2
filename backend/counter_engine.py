import random
import pandas as pd
import joblib
import os

# load model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "ml_core", "models", "battle_predictor.pkl")

model = joblib.load(MODEL_PATH)

# load feature columns
DATA_PATH = os.path.join(BASE_DIR, "ml_core", "data", "processed", "final_dataset.csv")
columns = pd.read_csv(DATA_PATH, nrows=1).columns

# build input row for model
def build_row(deckA, deckB):
    row = {col:0 for col in columns}

    for card in deckA:
        key = f"A_{card}"
        if key in row:
            row[key] = 1

    for card in deckB:
        key = f"B_{card}"
        if key in row:
            row[key] = 1

    return pd.DataFrame([row])

# get all usable card ids
ALL_CARDS = []

for col in columns:
    if col.startswith("A_"):
        part = col.split("_")[1]

        # only keep real card ids (numbers only)
        if part.isdigit():
            ALL_CARDS.append(int(part))

# random deck generator
def random_deck():
    return random.sample(ALL_CARDS, 8)

# evaluate win probability
def evaluate(candidate, enemy):
    X = build_row(candidate, enemy)
    prob = model.predict_proba(X)[0][1]
    return prob

# search best counter
def find_best_counter(enemy, iterations=300):

    best_deck = None
    best_score = 0

    for _ in range(iterations):
        deck = random_deck()
        score = evaluate(deck, enemy)

        if score > best_score:
            best_score = score
            best_deck = deck

    return best_deck, round(best_score*100, 2)