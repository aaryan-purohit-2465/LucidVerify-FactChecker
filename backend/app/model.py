# backend/app/model.py

model = None

def load_model():
    """
    Loads or initializes the model.
    This is a safe fallback model for now.
    """
    global model
    model = "rule_based_model"
    print("Model loaded successfully")


def predict(text: str):
    """
    Simple rule-based prediction (temporary but stable).
    """
    if not text or not text.strip():
        return {
            "label": "unknown",
            "confidence": 0.0,
            "source": "rule-based"
        }

    keywords = ["government", "policy", "minister", "election", "education"]
    text_lower = text.lower()

    if any(word in text_lower for word in keywords):
        return {
            "label": "real",
            "confidence": 0.8,
            "source": "rule-based"
        }

    return {
        "label": "unknown",
        "confidence": 0.4,
        "source": "rule-based"
    }
