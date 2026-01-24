import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "super_model.joblib")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.joblib")

model = None
vectorizer = None


def load_model():
    global model, vectorizer
    print("🔄 Loading ML model and vectorizer...")
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("✅ Model loaded successfully")


def predict(text: str):
    try:
        if not isinstance(text, str):
            return "error", 0.0, "invalid_input"

        # 🚫 DO NOT clean text manually
        # ✅ Vectorizer already knows how to process text
        vectorized = vectorizer.transform([text])

        prediction = model.predict(vectorized)[0]
        confidence = max(model.predict_proba(vectorized)[0])

        label = "Real" if prediction == 1 else "Fake"

        return label, round(float(confidence), 3), "ml_model"

    except Exception as e:
        return "error", 0.0, str(e)
