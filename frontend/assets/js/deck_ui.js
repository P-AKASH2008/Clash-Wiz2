const allCards = [
    26000000,26000001,26000002,26000003,26000004,
    26000005,26000006,26000007,26000008,26000009,
    26000010,26000011,26000012,26000013,26000014,
    26000015,26000016,26000017,26000018,26000019
];

let deckA = [];
let deckB = [];
let selectingDeck = "A";

const grid = document.getElementById("card-grid");
const deckASlots = document.getElementById("deckA-slots");
const deckBSlots = document.getElementById("deckB-slots");

function renderDeck(deck, container) {
    container.innerHTML = "";
    deck.forEach(card => {
        const div = document.createElement("div");
        div.className = "deck-card";
        div.innerText = card.toString().slice(-2);
        container.appendChild(div);
    });
}

allCards.forEach(card => {
    const div = document.createElement("div");
    div.className = "card-item";
    div.innerText = card.toString().slice(-2);

    div.onclick = () => {
        if (selectingDeck === "A" && deckA.length < 8) {
            deckA.push(card);
            renderDeck(deckA, deckASlots);
            if (deckA.length === 8) selectingDeck = "B";
        }
        else if (selectingDeck === "B" && deckB.length < 8) {
            deckB.push(card);
            renderDeck(deckB, deckBSlots);
        }
    };

    grid.appendChild(div);
});

document.querySelector(".predict-btn").onclick = async () => {

    if (deckA.length !== 8 || deckB.length !== 8) {
        alert("Both decks must have 8 cards!");
        return;
    }

    const result = await predictBattle(deckA, deckB);

    document.querySelector(".probability-text").innerText =
        `Deck A: ${result.deckA_win_probability}% | Deck B: ${result.deckB_win_probability}%`;

    document.querySelector(".deckA-bar").style.width =
        result.deckA_win_probability + "%";

    document.querySelector(".deckB-bar").style.width =
        result.deckB_win_probability + "%";
};