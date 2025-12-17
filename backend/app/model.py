import joblib

model = joblib.load("backend/app/baseline_model.pkl")
vectorizer = joblib.load("backend/app/tfidf_vectorizer.pkl")

def predict(text: str):
    X = vectorizer.transform([text])
    probs = model.predict_proba(X)[0]
    idx = probs.argmax()

    return {
        "label": str(model.classes_[idx]),
        "confidence": float(probs[idx]),
        "source": "baseline-ml"
    }
