import joblib
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "ml_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")

model = None
vectorizer = None


def load_model():
    global model, vectorizer

    try:
        print("Loading model from:", MODEL_PATH)
        print("Loading vectorizer from:", VECTORIZER_PATH)

        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)

        print("✅ Model loaded:", type(model))
        print("✅ Vectorizer loaded:", type(vectorizer))

        return True

    except Exception as e:
        print("❌ MODEL LOAD ERROR:", e)
        return False


def predict(text: str):
    try:
        if model is None or vectorizer is None:
            return {
                "label": "unknown",
                "confidence": 0.0,
                "source": "fallback"
            }

        X = vectorizer.transform([text])

        # Handle models without predict_proba
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X)[0]
            fake_prob = float(probs[0])
            real_prob = float(probs[1])
        else:
            pred = model.predict(X)[0]
            fake_prob = 1.0 if pred == 0 else 0.0
            real_prob = 1.0 if pred == 1 else 0.0

        if real_prob >= fake_prob:
            label = "real"
            confidence = real_prob
        else:
            label = "fake"
            confidence = fake_prob

        return {
            "label": label,
            "confidence": round(confidence, 2),
            "source": "ml_model"
        }

    except Exception as e:
        print("❌ PREDICTION ERROR:", e)
        return {
            "label": "error",
            "confidence": 0.0,
            "source": "server_error"
        }
