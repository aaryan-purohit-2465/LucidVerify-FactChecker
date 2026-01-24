import joblib
import os
import re
from typing import Tuple

MODEL_PATH = os.path.join(os.path.dirname(__file__), "super_model.joblib")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.joblib")

model = None
vectorizer = None


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_model():
    global model, vectorizer

    print("🔄 Loading ML model and vectorizer...")

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    print("✅ Model loaded successfully")


def predict(text: str) -> Tuple[str, float, str]:
    try:
        if model is None or vectorizer is None:
            return "error", 0.0, "model_not_loaded"

        cleaned = clean_text(text)

        # Vectorize ONLY after cleaning
        vectorized = vectorizer.transform([cleaned])

        prediction = model.predict(vectorized)[0]
        confidence = max(model.predict_proba(vectorized)[0])

        label = "Real" if prediction == 1 else "Fake"

        return label, round(float(confidence), 3), "ml_model"

    except Exception as e:
        return "error", 0.0, str(e)
