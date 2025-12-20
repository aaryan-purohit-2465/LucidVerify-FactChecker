# backend/app/model.py
# Simple, stable ML stub (no load_model, no crashes)

def predict(text: str):
    if not text or not isinstance(text, str):
        return {
            "label": "unknown",
            "confidence": 0.0,
            "source": "invalid-input"
        }

    text = text.lower()

    if any(word in text for word in ["fake", "hoax", "rumour", "rumor"]):
        return {
            "label": "fake",
            "confidence": 0.78,
            "source": "rule-based"
        }

    return {
        "label": "real",
        "confidence": 0.82,
        "source": "rule-based"
    }
