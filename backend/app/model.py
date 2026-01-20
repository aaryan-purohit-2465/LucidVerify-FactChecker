import joblib
import os
import numpy as np

MODEL_PATH = "backend/models/model.pkl"
VECTORIZER_PATH = "backend/models/vectorizer.pkl"

model = None
vectorizer = None


def load_model():
    global model, vectorizer

    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        print("❌ Model or vectorizer not found!")
        return False

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    print("✅ ML Model Loaded Successfully")
    return True


def predict(text):
    if model is None or vectorizer is None:
        return {
            "label": "unknown",
            "confidence": 0.0,
            "source": "fallback"
        }

    X = vectorizer.transform([text])
    probs = model.predict_proba(X)[0]

    fake_prob = probs[0]
    real_prob = probs[1]

    if real_prob > fake_prob:
        label = "real"
        confidence = real_prob
    else:
        label = "fake"
        confidence = fake_prob

    return {
        "label": label,
        "confidence": round(float(confidence), 2),
        "source": "ml_model"
    }
