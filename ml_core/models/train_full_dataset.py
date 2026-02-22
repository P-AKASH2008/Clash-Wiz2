import pandas as pd
import joblib
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import sys
import os

sys.path.append(os.path.abspath("../feature_engineering"))

from encode_cards import encode_deck

print("Loading raw dataset...")

df = pd.read_pickle("../data/raw/clash_matches.pkl")

# initialize model
model = XGBClassifier(
    n_estimators=40,        # small per batch
    max_depth=6,
    learning_rate=0.08,
    subsample=0.8,
    colsample_bytree=0.8,
    tree_method="hist",
    eval_metric="logloss",
    n_jobs=-1,
    use_label_encoder=False,
    warm_start=True
)

BATCH_SIZE = 50000
num_batches = len(df) // BATCH_SIZE

print("Total batches:", num_batches)

first_batch = True

for i in tqdm(range(num_batches)):

    batch = df.iloc[i*BATCH_SIZE:(i+1)*BATCH_SIZE]

    X_batch = []
    y_batch = []

    for _, row in batch.iterrows():
        deckA = encode_deck(row["deckA"])
        deckB = encode_deck(row["deckB"])

        X_batch.append(deckA + deckB)
        y_batch.append(row["label"])

    X_batch = np.array(X_batch)
    y_batch = np.array(y_batch)

    if first_batch:
        model.fit(X_batch, y_batch)
        first_batch = False
    else:
        model.fit(X_batch, y_batch, xgb_model=model)

print("Saving trained model...")
joblib.dump(model, "win_predictor.pkl")

print("FULL DATASET TRAINING COMPLETE ✅")