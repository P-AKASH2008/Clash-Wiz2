import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("Loading encoded dataset...")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data/processed/final_dataset.csv"

df = pd.read_csv(DATA_PATH)

# remove leakage if present
DROP_COLS = ["trophyA","trophyB","trophy_diff"]
for c in DROP_COLS:
    if c in df.columns:
        df = df.drop(columns=[c])

y = df["winner"]
X = df.drop(columns=["winner"])

# chronological split
split = int(len(df)*0.8)

X_train = X.iloc[:split]
X_test  = X.iloc[split:]

y_train = y.iloc[:split]
y_test  = y.iloc[split:]

print("Training model...")

model = RandomForestClassifier(
    n_estimators=140,
    max_depth=18,
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)

print("FINAL ACCURACY:", acc)

MODEL_PATH = BASE_DIR / "models/battle_predictor.pkl"
joblib.dump(model, MODEL_PATH)

print("Model saved at:", MODEL_PATH)