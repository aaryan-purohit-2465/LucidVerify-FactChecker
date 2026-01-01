# LucidVerify – Fact Checker 📰✅

LucidVerify is a full-stack fact-checking web application that analyzes user-submitted text and predicts whether the information is **Real** or **Fake**.  
The project is designed with a strong backend, clean API architecture, and a modern frontend UI, making it suitable for real-world usage and deployment.

---

## 🚀 Features

- 🔍 Text-based fact checking
- ⚙️ FastAPI backend with REST API
- 🧠 Rule-based prediction logic (ML-ready architecture)
- 🎨 Modern frontend using React + HTML + CSS
- 🌐 CORS-enabled backend for frontend integration
- 📡 Real-time API communication
- 🧩 Scalable structure for future ML/Transformer models

---

## 🏗️ Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn

### Frontend
- React (Vite)
- HTML5
- CSS3
- JavaScript

---

## 📂 Project Structure

LucidVerify-FactChecker/
│
├── backend/
│ └── app/
│ ├── main.py
│ └── model.py
│
├── frontend/
│ ├── src/
│ ├── index.html
│ └── package.json
│
├── .gitignore
├── README.md
└── requirements.txt

---

## ▶️ How to Run Locally

### Backend
```bash
py -3 -m uvicorn backend.app.main:app --reload
API will run at:

http://127.0.0.1:8000

Frontend
cd frontend
npm run dev


Frontend will run at:

http://localhost:5173

🔗 API Endpoint

POST /predict

Request Body

{
  "text": "Government announces new education reforms"
}


Response

{
  "label": "real",
  "confidence": 0.8,
  "source": "rule-based"
}

🛠️ Current Status

✅ Backend API stable
✅ Frontend connected to backend
✅ Prediction pipeline working

🔄 UI enhancements and ML model upgrades in progress

📌 Future Improvements

Integration of ML models (TF-IDF, Transformers)

Source-based verification

Confidence visualization

User authentication

Cloud deployment

👨‍💻 Author

Aaryan Purohit
Computer Science Student

⭐ If you find this project interesting, feel free to star the repository!