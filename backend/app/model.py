def predict(text: str):
    text = text.lower()

    fake_keywords = [
        "fake", "hoax", "rumor", "false", "misleading",
        "scam", "clickbait", "unverified"
    ]

    if any(word in text for word in fake_keywords):
        return {
            "label": "fake",
            "confidence": 0.80,
            "source": "rule-based"
        }

    return {
        "label": "real",
        "confidence": 0.80,
        "source": "rule-based"
    }
