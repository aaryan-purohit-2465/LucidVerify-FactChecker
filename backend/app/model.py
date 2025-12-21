# backend/app/model.py
# Safe, crash-proof model layer

_model = None
_vectorizer = None

def load_model():
    """
    Safe loader.
    If model files exist later, we can load them here.
    For now, keep backend stable.
    """
    global _model, _vectorizer
    _model = None
    _vectorizer = None
    print("✅ load_model() called — no ML model loaded (safe mode)")


def predict(text: str):
    """
    Always returns a valid response.
    NEVER crashes the API.
    """
    if not text or not isinstance(text, str):
        return {
            "label": "unknown",
            "confidence": 0.0,
            "source": "fallback"
        }

    text = text.lower()

    if "fake" in text or "hoax" in text or "rumor" in text:
        return {
            "label": "fake",
            "confidence": 0.75,
            "source": "rule-based"
        }

    return {
        "label": "real",
        "confidence": 0.80,
        "source": "rule-based"
    }
    