from backend.services.model_service import ModelService

model_service = ModelService()

def evaluate_battle(deckA, deckB):
    probs = model_service.predict_probability(deckA, deckB)

    winner = "Player A" if probs["probabilityA"] > probs["probabilityB"] else "Player B"

    return {
        "winner": winner,
        "probabilityA": round(probs["probabilityA"] * 100, 2),
        "probabilityB": round(probs["probabilityB"] * 100, 2)
    }