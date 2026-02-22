document.addEventListener("DOMContentLoaded", function () {

/* EVERYTHING goes inside this */

let currentDeck = "A";
let selectedSlot = null;

const deckA = new Array(8).fill(null);
const deckB = new Array(8).fill(null);

/* create empty slots */
function createSlots() {
    const deckAContainer = document.getElementById("deckA");
    const deckBContainer = document.getElementById("deckB");

    for (let i = 0; i < 8; i++) {

        const slotA = document.createElement("div");
        slotA.className = "slot";
        slotA.dataset.index = i;
        slotA.onclick = () => {
            selectedSlot = {team:"A", element:slotA, index:i};
            console.log("Selected Team A slot", i);
        };
        deckAContainer.appendChild(slotA);

        const slotB = document.createElement("div");
        slotB.className = "slot";
        slotB.dataset.index = i;
        slotB.onclick = () => {
            selectedSlot = {team:"B", element:slotB, index:i};
            console.log("Selected Team B slot", i);
        };
        deckBContainer.appendChild(slotB);
    }
}

/* slug converter */
function toSlug(name){
    return name
        .toLowerCase()
        .replace(/\./g, '')
        .replace(/ /g, '-')
        .replace(/'/g, '');
}

/* load card list */
let cards = [];

async function loadCards(){
    const res = await fetch("data/cards.json");
    cards = await res.json();
    console.log("Cards loaded:", cards.length);
}

/* search bar */
document.getElementById("cardSearch").addEventListener("input", function(){

    const query = this.value.toLowerCase();
    const results = document.getElementById("searchResults");
    results.innerHTML = "";

    if(query.length === 0) return;

    cards
        .filter(c => c.name.toLowerCase().includes(query))
        .slice(0, 20)
        .forEach(card => {

            const div = document.createElement("div");
            div.className = "search-item";
            div.innerText = card.name;

            div.onclick = () => selectCard(card);

            results.appendChild(div);
        });
});

/* selecting card */
function selectCard(card){

    if(!selectedSlot){
        alert("Click a slot first!");
        return;
    }

    const img = document.createElement("img");
    const slug = toSlug(card.name);

    img.src =
    `https://raw.githubusercontent.com/RoyaleAPI/cr-api-assets/master/cards-150-gold/${slug}.png`;

    selectedSlot.element.innerHTML = "";
    selectedSlot.element.appendChild(img);

    if(selectedSlot.team === "A")
        deckA[selectedSlot.index] = parseInt(card.id);
    else
        deckB[selectedSlot.index] = parseInt(card.id);

    console.log("DeckA:", deckA);
    console.log("DeckB:", deckB);
}

/* predict button */
document.getElementById("predictBtn").onclick = async () => {

    if(deckA.includes(null) || deckB.includes(null)){
        alert("Fill all 8 cards for both teams!");
        return;
    }

    const res = await fetch("http://127.0.0.1:5000/predict",{
        method:"POST",
        headers:{ "Content-Type":"application/json"},
        body: JSON.stringify({deckA, deckB})
    });

    const data = await res.json();

    document.getElementById("resultBox").innerHTML =
        `Winner: ${data.data.winner}<br>
         Team A: ${data.data.probabilityA}%<br>
         Team B: ${data.data.probabilityB}%`;
};

createSlots();
loadCards();

});