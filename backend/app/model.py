import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "super_model.joblib")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.joblib")

model = None
vectorizer = None


def load_model():
    global model, vectorizer

    if model is None or vectorizer is None:
        print("🔄 Loading ML model and vectorizer...")
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        print("✅ Model loaded successfully")


def predict(text: str):
    if not model or not vectorizer:
        raise RuntimeError("Model not loaded")

    text_vec = vectorizer.transform([text])
    probs = model.predict_proba(text_vec)[0]

    label_index = np.argmax(probs)
    confidence = float(probs[label_index])

    label = "Real" if label_index == 1 else "Fake"

    return {
        "label": label,
        "confidence": round(confidence, 3),
        "source": "ml_super_model"
    }
