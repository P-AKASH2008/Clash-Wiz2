const deckAContainer = document.getElementById("deckA");
const deckBContainer = document.getElementById("deckB");
const cardLibrary = document.getElementById("cardLibrary");
const resultBox = document.getElementById("resultBox");

// Create 8 slots each
for(let i=0;i<8;i++){
    createSlot(deckAContainer);
    createSlot(deckBContainer);
}

function createSlot(container){
    const slot = document.createElement("div");
    slot.className = "slot";
    slot.ondragover = e => e.preventDefault();
    slot.ondrop = dropCard;
    container.appendChild(slot);
}

let draggedCardId = null;

function dragCard(e){
    draggedCardId = e.target.dataset.id;
}

function dropCard(e){
    if(!draggedCardId) return;

    e.target.innerHTML = "";
    const img = document.createElement("img");
    img.src = "assets/images/cards/" + draggedCardId + ".png";
    img.width = 90;
    img.height = 120;
    e.target.appendChild(img);
    e.target.dataset.id = draggedCardId;
}

// Load cards
fetch("data/cards.json")
.then(res => res.json())
.then(cards => {
    cards.forEach(card => {
        const img = document.createElement("img");
        img.src = "assets/images/cards/" + card.id + ".png";
        img.className = "card";
        img.draggable = true;
        img.dataset.id = card.id;
        img.ondragstart = dragCard;
        cardLibrary.appendChild(img);
    });
});

// Predict
document.getElementById("predictBtn").addEventListener("click", async function(){

    const deckA = [...deckAContainer.children]
        .map(s => parseInt(s.dataset.id))
        .filter(Boolean);

    const deckB = [...deckBContainer.children]
        .map(s => parseInt(s.dataset.id))
        .filter(Boolean);

    if(deckA.length !== 8 || deckB.length !== 8){
        alert("Both teams must have 8 cards.");
        return;
    }

    resultBox.innerHTML = "Analyzing battle...";

    const response = await fetch("http://127.0.0.1:5000/predict",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ deckA, deckB })
    });

    const data = await response.json();

    resultBox.innerHTML =
        `<h2>${data.winner} Favored</h2>
         <p>Team A: ${data.probabilityA}%</p>
         <p>Team B: ${data.probabilityB}%</p>`;
});