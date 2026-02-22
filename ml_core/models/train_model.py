import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("Loading encoded dataset...")

# ---------------------------------------------------
# Paths
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data/processed/final_dataset.csv"
MODEL_PATH = BASE_DIR / "models/battle_predictor.pkl"

# ---------------------------------------------------
# Load dataset
# ---------------------------------------------------
df = pd.read_csv(DATA_PATH)

print("Dataset rows:", len(df))
print("Dataset columns:", len(df.columns))

# ---------------------------------------------------
# REMOVE LEAKAGE (VERY IMPORTANT)
# ---------------------------------------------------
LEAK_COLS = ["trophyA", "trophyB", "trophy_diff"]

for col in LEAK_COLS:
    if col in df.columns:
        df = df.drop(columns=[col])
        print("Removed leakage column:", col)

# ---------------------------------------------------
# Separate features and label
# ---------------------------------------------------
y = df["winner"]
X = df.drop(columns=["winner"])

print("Total features used:", X.shape[1])

# ---------------------------------------------------
# Chronological split (prevents same battles in train/test)
# ---------------------------------------------------
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test  = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test  = y.iloc[split_index:]

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# ---------------------------------------------------
# Train Model
# ---------------------------------------------------
print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=160,      # number of trees
    max_depth=18,          # prevents overfitting
    min_samples_leaf=2,    # smoother probabilities
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------------------------------------------
# Evaluate
# ---------------------------------------------------
print("\nEvaluating model...")

preds = model.predict(X_test)
accuracy = accuracy_score(y_test, preds)

print("\nFINAL ACCURACY:", round(accuracy * 100, 2), "%")

# ---------------------------------------------------
# Save model
# ---------------------------------------------------
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("Model saved at:", MODEL_PATH)

# ---------------------------------------------------
# Quick probability sanity check
# ---------------------------------------------------
print("\nProbability sanity check:")

sample_probs = model.predict_proba(X_test.iloc[:5])
for i, p in enumerate(sample_probs):
    print(f"Match {i+1} -> PlayerA: {round(p[1]*100,2)}% | PlayerB: {round(p[0]*100,2)}%")

print("\nTraining complete ✔")