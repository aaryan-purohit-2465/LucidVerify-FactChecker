# backend/app/model.py

import joblib
import os

MODEL_PATH = "backend/app/baseline_model.pkl"
VECTORIZER_PATH = "backend/app/tfidf_vectorizer.pkl"

model = None
vectorizer = None


def load_model():
    """
    Loads ML model and vectorizer into memory.
    Called once on app startup.
    """
    global model, vectorizer

    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        print("⚠️ Model files not found, running in fallback mode")
        model = None
        vectorizer = None
        return

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("✅ ML model loaded successfully")


def predict(text: str):
    """
    Predicts label for given text.
    """
    if model is None or vectorizer is None:
        return {
            "label": "unknown",
            "confidence": 0.0,
            "source": "fallback"
        }

    X = vectorizer.transform([text])
    probs = model.predict_proba(X)[0]
    idx = probs.argmax()

    return {
        "label": str(model.classes_[idx]),
        "confidence": float(probs[idx]),
        "source": "baseline-ml"
    }
