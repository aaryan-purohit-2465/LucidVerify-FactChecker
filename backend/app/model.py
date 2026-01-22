import joblib
import os
import numpy as np

# Base directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.joblib")

model = None
vectorizer = None


def load_model():
    global model, vectorizer

    if model is None or vectorizer is None:
        print("Loading trained ML model...")

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("model.joblib not found")

        if not os.path.exists(VECTORIZER_PATH):
            raise FileNotFoundError("vectorizer.joblib not found")

        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)

        print("Model loaded successfully!")


def predict(text: str):
    if not text or len(text.strip()) < 10:
        return {
            "label": "Uncertain",
            "confidence": 0.0,
            "source": "ml_model",
            "message": "Text too short for reliable prediction"
        }

    if model is None or vectorizer is None:
        load_model()

    # Vectorize input
    vectorized = vectorizer.transform([text])

    # Prediction
    prediction = model.predict(vectorized)[0]
    probs = model.predict_proba(vectorized)[0]

    confidence = float(np.max(probs))

    label = "Real" if prediction == 1 else "Fake"

    # Low confidence handling
    if confidence < 0.65:
        label = "Uncertain"

    return {
        "label": label,
        "confidence": round(confidence, 4),
        "source": "ml_model"
    }
