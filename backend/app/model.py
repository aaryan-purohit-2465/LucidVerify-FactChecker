import pickle
import numpy as np

with open("backend/app/ml_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("backend/app/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


def predict(text: str):
    vec = vectorizer.transform([text])
    probs = model.predict_proba(vec)[0]
    prediction = model.classes_[probs.argmax()]
    confidence = float(probs.max())

    # Explainability
    feature_names = vectorizer.get_feature_names_out()
    coef = model.coef_[0]

    word_scores = vec.toarray()[0] * coef
    top_indices = np.argsort(word_scores)[-3:]

    keywords = [feature_names[i] for i in top_indices if word_scores[i] > 0]

    return {
        "label": prediction,
        "confidence": round(confidence, 2),
        "source": "ml-model",
        "keywords": keywords
    }
