from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from pathlib import Path

# ----------------------------
# Setup App
# ----------------------------
app = Flask(__name__)
CORS(app)  # allows frontend to call backend

# ----------------------------
# Load Model
# ----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "ml_core/models/battle_predictor.pkl"
DATA_PATH = BASE_DIR / "ml_core/data/processed/final_dataset.csv"

model = joblib.load(MODEL_PATH)

# Load column structure from dataset
df_columns = pd.read_csv(DATA_PATH, nrows=1).columns
feature_columns = [c for c in df_columns if c != "winner"]

# ----------------------------
# Helper: Build Feature Vector
# ----------------------------
def build_feature_row(deckA, deckB):
    row = pd.Series(0, index=feature_columns)

    for cid in deckA:
        col = f"A_{cid}"
        if col in row.index:
            row[col] = 1

    for cid in deckB:
        col = f"B_{cid}"
        if col in row.index:
            row[col] = 1

    return row


# ----------------------------
# Health Check
# ----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "Backend running"
    })


# ----------------------------
# Predict Endpoint
# ----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    deckA = data.get("deckA")
    deckB = data.get("deckB")

    if not isinstance(deckA, list) or not isinstance(deckB, list):
        return jsonify({"error": "Decks must be lists"}), 400

    if len(deckA) != 8 or len(deckB) != 8:
        return jsonify({"error": "Each deck must contain 8 cards"}), 400

    try:
        row = build_feature_row(deckA, deckB)
        probs = model.predict_proba([row.values])[0]

        result = {
            "winner": "Player A" if probs[1] > probs[0] else "Player B",
            "probabilityA": round(float(probs[1]) * 100, 2),
            "probabilityB": round(float(probs[0]) * 100, 2)
        }

        return jsonify({"data": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)