from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os

# -------------------------
# App Setup
# -------------------------

app = FastAPI()

# Allow all origins (for dev + prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Load Model & Vectorizer
# -------------------------

MODEL_PATH = "backend/app/model.joblib"
VECTORIZER_PATH = "backend/app/vectorizer.joblib"

print("🔄 Loading ML model and vectorizer...")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

print("✅ Model loaded successfully")

# -------------------------
# Request Schema
# -------------------------

class NewsRequest(BaseModel):
    text: str

# -------------------------
# Routes
# -------------------------

@app.get("/")
def root():
    return {"message": "LucidVerify API is running"}

@app.post("/predict")
def predict_news(req: NewsRequest):
    text = req.text

    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X).max()

    label = "real" if pred == 1 else "fake"

    return {
        "label": label,
        "confidence": round(float(prob), 3),
        "source": "ml_model"
    }
