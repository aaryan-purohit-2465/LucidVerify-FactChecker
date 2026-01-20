def rule_based_check(text):
    suspicious_words = [
        "shocking", "breaking", "exposed", "secret", "miracle",
        "you won't believe", "viral", "click here", "guaranteed"
    ]

    text_lower = text.lower()

    for word in suspicious_words:
        if word in text_lower:
            return {
                "label": "fake",
                "confidence": 0.85,
                "source": "rule_based"
            }

    return None
