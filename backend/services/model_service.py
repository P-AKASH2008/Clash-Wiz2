import joblib
import pandas as pd
from backend.config import MODEL_PATH, DATASET_PATH

class ModelService:

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.columns = self._load_columns()

    def _load_columns(self):
        df = pd.read_csv(DATASET_PATH, nrows=1)
        return [c for c in df.columns if c != "winner"]

    def build_feature_row(self, deckA, deckB):
        row = pd.Series(0, index=self.columns)

        for cid in deckA:
            col = f"A_{cid}"
            if col in row.index:
                row[col] = 1

        for cid in deckB:
            col = f"B_{cid}"
            if col in row.index:
                row[col] = 1

        return row

    def predict_probability(self, deckA, deckB):
        row = self.build_feature_row(deckA, deckB)
        probs = self.model.predict_proba([row.values])[0]

        return {
            "probabilityA": float(probs[1]),
            "probabilityB": float(probs[0])
        }