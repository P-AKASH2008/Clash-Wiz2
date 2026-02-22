from flask import Blueprint, request, jsonify
from backend.services.predict_service import evaluate_battle
from backend.utils.validators import validate_deck
from backend.utils.response_builder import success_response, error_response

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():

    data = request.json

    if not data:
        return jsonify(error_response("No JSON body provided")), 400

    deckA = data.get("deckA")
    deckB = data.get("deckB")

    validA, errorA = validate_deck(deckA)
    validB, errorB = validate_deck(deckB)

    if not validA:
        return jsonify(error_response(errorA)), 400

    if not validB:
        return jsonify(error_response(errorB)), 400

    result = evaluate_battle(deckA, deckB)

    return jsonify(success_response(result))