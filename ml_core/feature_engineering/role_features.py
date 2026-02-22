import json
import os

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../config/card_metadata.json"
)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cards = json.load(f)

# Build lookup: card_id -> troop_type
CARD_TYPE = {}

for card in cards:
    card_id = int(card["id"])
    troop_type = card.get("troop_type", "").lower()
    CARD_TYPE[card_id] = troop_type


def deck_type_counts(deck):
    troops = 0
    spells = 0
    buildings = 0

    for c in deck:
        t = CARD_TYPE.get(c, "")

        if t == "troop":
            troops += 1
        elif t == "spell":
            spells += 1
        elif t == "building":
            buildings += 1

    return troops, spells, buildings