import pickle

# Load model and vectorizer once
with open("backend/app/ml_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("backend/app/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


def predict(text: str):
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    confidence = max(model.predict_proba(vec)[0])

    return {
        "label": prediction,
        "confidence": round(float(confidence), 2),
        "source": "ml-model"
    }
