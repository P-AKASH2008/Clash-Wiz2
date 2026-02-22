# 🧠 ClashWiz – AI Powered Clash Royale Strategy Assistant

ClashWiz is a Machine Learning powered web application that helps players:

- 🔮 Predict battle outcomes between two decks  
- 🛡 Generate the best counter deck against an enemy deck  
- 📊 Analyze win probabilities using a trained ML model  
- 🎮 Interact with a Clash‑style deck building interface  

---

# 🚀 Features

## ⚔ Battle Prediction
- Select 8 cards for Team A  
- Select 8 cards for Team B  
- Get win probability for both teams  
- ML-based probabilistic outcome prediction  

📸 Screenshot:
<img width="1907" height="1141" alt="image" src="https://github.com/user-attachments/assets/5152cb8a-0bf6-4474-b193-663705753edc" />


---

## 🛡 Counter Deck Generator
- Input enemy deck (8 cards)  
- AI simulates hundreds of candidate decks  
- Returns the best-performing counter deck  
- Displays expected win percentage  

📸 Screenshot:
<img width="1919" height="1140" alt="image" src="https://github.com/user-attachments/assets/8ae20c06-c841-48c9-857f-c488020317e0" />

---

# 🏗 Project Structure

Clash-Wiz2/
│
├── backend/
│   ├── app.py
│   └── counter_engine.py
│
├── frontend/
│   ├── index.html
│   ├── predict.html
│   ├── deck_builder.html
│   ├── predict.js
│   ├── counter.js
│   ├── data/
│   │   └── cards.json
│   └── assets/
│       └── css/
│           ├── style.css
│           └── predict.css
│
├── ml_core/
│   ├── models/
│   │   └── battle_predictor.pkl
│   └── data/
│       └── processed/
│           └── final_dataset.csv
│
└── README.md

---

# 🧠 Machine Learning Architecture

### Model Type
Classification Model (Random Forest / Logistic Regression)

### Input Representation
- One-hot encoded deck vectors
- Format example:
  - A_26000021 → Player A has Hog Rider  
  - B_26000021 → Player B has Hog Rider  

### Output
- Probability Player A wins  
- Probability Player B wins  

---

# 🛡 Counter Deck Logic

Instead of training a second ML model, ClashWiz uses a Monte Carlo Search strategy:

1. Generate random candidate decks  
2. Simulate battle vs enemy deck  
3. Use trained ML model to compute win probability  
4. Repeat hundreds of times  
5. Return deck with highest win chance  

This converts the prediction model into a recommendation engine.

---

# 🖥️ How To Run

## 1️⃣ Install Dependencies

pip install flask flask-cors pandas scikit-learn joblib

---

## 2️⃣ Start Backend

From project root:

py backend/app.py

You should see:

Running on http://127.0.0.1:5000

---

## 3️⃣ Start Frontend

Open another terminal:

cd frontend  
python -m http.server 5500

---

## 4️⃣ Open Website

Go to:

http://localhost:5500

---

# 📊 Future Improvements

- Genetic Algorithm based deck optimization  
- Meta analysis dashboard  
- Card synergy scoring  
- User authentication & saved decks  
- Cloud deployment (Render / Railway)  

---

# 👨‍💻 Authors

Mahesh Chandaluri  
Suhas Lankapalli  
P. Akash  

---

# 📸 Demo Screens

🏠 Home Page  
<img width="1919" height="1138" alt="image" src="https://github.com/user-attachments/assets/93cc53f6-3382-43d1-97fb-5057244abf4c" />
