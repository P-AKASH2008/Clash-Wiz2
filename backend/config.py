from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "ml_core/models/battle_predictor.pkl"
DATASET_PATH = BASE_DIR / "ml_core/data/processed/final_dataset.csv"

DEBUG = True
HOST = "127.0.0.1"
PORT = 5000
