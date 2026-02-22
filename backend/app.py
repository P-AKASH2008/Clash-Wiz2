proba = model.predict_proba([match_vector])[0]

deckA_prob = float(proba[1])
deckB_prob = float(proba[0])

return jsonify({
    "deckA_win_probability": round(deckA_prob * 100, 2),
    "deckB_win_probability": round(deckB_prob * 100, 2)
})