import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "super_model.joblib")

model = None


def load_model():
    global model
    print("🔄 Loading ML pipeline model...")
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")


def predict(text: str):
    try:
        if model is None:
            return "error", 0.0, "model_not_loaded"

        if not isinstance(text, str):
            return "error", 0.0, "invalid_input"

        # ✅ PIPELINE HANDLES EVERYTHING
        prediction = model.predict([text])[0]
        confidence = max(model.predict_proba([text])[0])

        label = "Real" if prediction == 1 else "Fake"

        return label, round(float(confidence), 3), "ml_model"

    except Exception as e:
        return "error", 0.0, str(e)
