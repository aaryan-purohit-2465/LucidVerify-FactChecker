import re

def analyze_text(text: str):
    text = text.lower()

    fake_keywords = [
        "shocking", "breaking", "you won't believe", "secret", "exposed",
        "miracle", "cure", "guaranteed", "click here", "hoax"
    ]

    real_keywords = [
        "government", "minister", "official", "report", "study",
        "announced", "released", "confirmed", "policy", "court"
    ]

    fake_score = 0
    real_score = 0

    for word in fake_keywords:
        if word in text:
            fake_score += 1

    for word in real_keywords:
        if word in text:
            real_score += 1

    if fake_score > real_score:
        label = "fake"
        confidence = min(0.6 + fake_score * 0.1, 0.95)
        explanation = "Detected sensational or misleading language patterns."
    elif real_score > fake_score:
        label = "real"
        confidence = min(0.6 + real_score * 0.1, 0.95)
        explanation = "Detected official or factual language patterns."
    else:
        label = "unknown"
        confidence = 0.5
        explanation = "Not enough information to determine authenticity."

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "source": "AI rule-engine",
        "explanation": explanation
    }
