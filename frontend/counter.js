document.addEventListener("DOMContentLoaded", function(){

let selectedSlot = null;
let lastSelected = null;

const enemyDeck = new Array(8).fill(null);

function createSlots(){
    const enemyContainer = document.getElementById("enemyDeck");
    const counterContainer = document.getElementById("counterDeck");

    for(let i=0;i<8;i++){

        const slot = document.createElement("div");
        slot.className = "slot";
        slot.onclick = () => {
            if(lastSelected) lastSelected.classList.remove("selected");
            slot.classList.add("selected");
            lastSelected = slot;
            selectedSlot = {index:i, element:slot};
        };
        enemyContainer.appendChild(slot);

        const resultSlot = document.createElement("div");
        resultSlot.className = "slot";
        counterContainer.appendChild(resultSlot);
    }
}

function toSlug(name){
    return name
        .toLowerCase()
        .replace(/\./g, '')
        .replace(/ /g, '-')
        .replace(/'/g, '');
}

let cards = [];

async function loadCards(){
    const res = await fetch("data/cards.json");
    cards = await res.json();
}

document.getElementById("cardSearch").addEventListener("input", function(){

    const query = this.value.toLowerCase();
    const results = document.getElementById("searchResults");
    results.innerHTML = "";

    if(query.length === 0) return;

    cards.filter(c => c.name.toLowerCase().includes(query))
         .slice(0,20)
         .forEach(card => {

            const div = document.createElement("div");
            div.className = "search-item";
            div.innerText = card.name;

            div.onclick = () => {

                if(!selectedSlot){
                    alert("Select a slot first");
                    return;
                }

                const slug = toSlug(card.name);
                const img = document.createElement("img");
                img.src =
                `https://raw.githubusercontent.com/RoyaleAPI/cr-api-assets/master/cards-150-gold/${slug}.png`;

                selectedSlot.element.innerHTML = "";
                selectedSlot.element.appendChild(img);

                enemyDeck[selectedSlot.index] = parseInt(card.id);

                selectedSlot.element.classList.remove("selected");
                selectedSlot = null;
            };

            results.appendChild(div);
         });
});

document.getElementById("generateBtn").onclick = async () => {

    if(enemyDeck.includes(null)){
        alert("Fill all 8 enemy cards!");
        return;
    }

    const res = await fetch("http://127.0.0.1:5000/counter",{
        method:"POST",
        headers:{ "Content-Type":"application/json"},
        body: JSON.stringify({enemyDeck})
    });

    const data = await res.json();

    const counterSlots = document.getElementById("counterDeck").children;

    data.counterDeck.forEach((id, i) => {

        const card = cards.find(c => parseInt(c.id) === id);
        const slug = toSlug(card.name);

        const img = document.createElement("img");
        img.src =
        `https://raw.githubusercontent.com/RoyaleAPI/cr-api-assets/master/cards-150-gold/${slug}.png`;

        counterSlots[i].innerHTML = "";
        counterSlots[i].appendChild(img);
    });

    document.getElementById("resultBox").innerHTML =
        `Expected Win Chance: ${data.winChance}%`;
};

createSlots();
loadCards();

});