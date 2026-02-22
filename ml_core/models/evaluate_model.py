import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score
import sys
import os

# allow access to encoder
sys.path.append(os.path.abspath("../feature_engineering"))
from encode_cards import encode_deck

print("Loading trained model...")
model = joblib.load("win_predictor.pkl")

print("Loading dataset sample...")
df = pd.read_pickle("../data/raw/clash_matches.pkl")

# we don't need whole dataset → just sample
test_df = df.sample(50000, random_state=1)

print("Preparing evaluation data...")

X_test = []
y_test = []

for _, row in test_df.iterrows():
    deckA = encode_deck(row["deckA"])
    deckB = encode_deck(row["deckB"])

    X_test.append(deckA + deckB)
    y_test.append(row["label"])

X_test = np.array(X_test)
y_test = np.array(y_test)

print("Running predictions...")
preds = model.predict(X_test)

acc = accuracy_score(y_test, preds)

print("\n==============================")
print("MODEL EVALUATION RESULT")
print("Accuracy:", round(acc * 100, 2), "%")
print("==============================")