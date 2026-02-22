def validate_deck(deck):

    if not isinstance(deck, list):
        return False, "Deck must be a list"

    if len(deck) != 8:
        return False, "Deck must contain exactly 8 cards"

    if not all(isinstance(x, int) for x in deck):
        return False, "All card IDs must be integers"

    return True, None