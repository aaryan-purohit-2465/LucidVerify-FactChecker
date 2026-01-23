import joblib
import os
import re
import numpy as np
from sklearn.exceptions import NotFittedError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.joblib")

model = None
vectorizer = None


# ---------------------------
# Text preprocessing (ONLY for raw string)
# ---------------------------
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------
# Load model + vectorizer
# ---------------------------
def load_model():
    global model, vectorizer

    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Model or vectorizer not found")

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    print("✅ ML model & vectorizer loaded successfully")


# ---------------------------
# Prediction
# ---------------------------
def predict(text: str):
    global model, vectorizer

    if model is None or vectorizer is None:
        return {
            "label": "error",
            "confidence": 0.0,
            "source": "server_error",
            "message": "model not loaded",
        }

    try:
        # 1️⃣ Clean RAW string
        cleaned = clean_text(text)

        # 2️⃣ Vectorize ONCE
        X = vectorizer.transform([cleaned])

        # 3️⃣ Predict
        prediction = model.predict(X)[0]
        confidence = float(np.max(model.predict_proba(X)))

        label = "Real" if prediction == 1 else "Fake"

        return {
            "label": label,
            "confidence": round(confidence, 3),
            "source": "ml_model",
        }

    except Exception as e:
        return {
            "label": "error",
            "confidence": 0.0,
            "source": "server_error",
            "message": str(e),
        }
