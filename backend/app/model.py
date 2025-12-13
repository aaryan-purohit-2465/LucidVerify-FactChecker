# backend/app/model.py

def predict(text: str):
    text = text.lower()

    if any(word in text for word in ["fake", "hoax", "rumor"]):
        return {
            "label": "fake",
            "confidence": 0.75,
            "source": "rule-based"
        }
    else:
        return {
            "label": "real",
            "confidence": 0.80,
            "source": "rule-based"
        }
