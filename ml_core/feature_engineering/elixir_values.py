import json
import os

# Load metadata file
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../config/card_metadata.json"
)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Build card_id → elixir mapping
ELIXIR_MAP = {}

for card in metadata:
    card_id = int(card["id"])
    elixir_cost = card["elixir"]

    ELIXIR_MAP[card_id] = elixir_cost


def deck_elixir(deck):
    total = 0
    count = 0

    for card in deck:
        if card in ELIXIR_MAP:
            total += ELIXIR_MAP[card]
            count += 1

    if count == 0:
        return 4  # neutral fallback

    return total / count