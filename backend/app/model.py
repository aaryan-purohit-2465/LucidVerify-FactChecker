# backend/app/model.py
"""
Model loader and prediction function for the LucidVerify API.

This file will:
 - Try to load a small baseline sklearn model + tfidf vectorizer from pickle files.
 - Try to load a transformer model from a local folder (optional).
 - Expose a top-level `predict(text: str) -> dict` function that returns:
    {"label": "...", "confidence": float, "source": "baseline"|"transformer"|"fallback", "message": "..."}
"""

import logging
import os
import pickle
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

logger = logging.getLogger("backend.app.model")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(ch)

ROOT = Path(__file__).parent.resolve()
BASELINE_PKL = ROOT / "baseline_model.pkl"
TFIDF_PKL = ROOT / "tfidf_vectorizer.pkl"
TRANSFORMER_DIRS = [
    ROOT / "roberta_final",
    ROOT / "roberta_model",
    ROOT / "roberta"  # try a few possible folder names
]

# Global holders
_baseline_model = None
_tfidf_vectorizer = None
_transformer = None
_transformer_tokenizer = None


def _load_baseline() -> None:
    global _baseline_model, _tfidf_vectorizer
    try:
        if BASELINE_PKL.exists() and TFIDF_PKL.exists():
            logger.info("Loading baseline model from: %s", BASELINE_PKL)
            with open(BASELINE_PKL, "rb") as f:
                _baseline_model = pickle.load(f)
            logger.info("Loaded baseline model: %s", type(_baseline_model).__name__)
            logger.info("Loading TF-IDF vectorizer from: %s", TFIDF_PKL)
            with open(TFIDF_PKL, "rb") as f:
                _tfidf_vectorizer = pickle.load(f)
            logger.info("Loaded TF-IDF vectorizer: %s", type(_tfidf_vectorizer).__name__)
        else:
            logger.info("Baseline model or TF-IDF not found (expected at %s and %s).",
                        BASELINE_PKL, TFIDF_PKL)
    except Exception as e:
        logger.exception("Failed to load baseline model or vectorizer: %s", e)
        _baseline_model = None
        _tfidf_vectorizer = None


def _load_transformer() -> None:
    """
    Try to load a local transformers model (fast path). This is optional.
    If transformers is not installed or the model directory is missing/corrupt, keep None.
    """
    global _transformer, _transformer_tokenizer
    try:
        # lazy import to avoid runtime dependency unless used
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
    except Exception as e:
        logger.info("Transformers not available or import failed: %s", e)
        return

    for d in TRANSFORMER_DIRS:
        if d.exists() and d.is_dir():
            try:
                logger.info("Attempting to load transformer model from: %s", d)
                _transformer_tokenizer = AutoTokenizer.from_pretrained(str(d))
                _transformer = AutoModelForSequenceClassification.from_pretrained(str(d))
                logger.info("Loaded transformer model and tokenizer from %s", d)
                return
            except Exception as e:
                logger.exception("Failed to load transformer model from %s: %s", d, e)
                _transformer = None
                _transformer_tokenizer = None
    logger.info("No transformer model folder found in %s", TRANSFORMER_DIRS)


# Load at import time (so uvicorn will run this as app starts)
try:
    _load_baseline()
    _load_transformer()
except Exception as e:
    logger.exception("Unexpected error while loading models: %s", e)


def _predict_baseline(text: str) -> Optional[Dict[str, Any]]:
    """Return prediction from baseline model if available."""
    if _baseline_model is None or _tfidf_vectorizer is None:
        return None
    try:
        X = _tfidf_vectorizer.transform([text])
        # Depending on your model, it may have predict_proba or decision_function
        if hasattr(_baseline_model, "predict_proba"):
            probs = _baseline_model.predict_proba(X)[0]
            # take argmax
            idx = int(probs.argmax())
            confidence = float(probs[idx])
            label = str(idx)
        else:
            pred = _baseline_model.predict(X)[0]
            confidence = 1.0
            label = str(pred)
        return {"label": label, "confidence": confidence, "source": "baseline"}
    except Exception as e:
        logger.exception("Baseline prediction failed: %s", e)
        return None


def _predict_transformer(text: str) -> Optional[Dict[str, Any]]:
    """Return transformer model prediction if available."""
    if _transformer is None or _transformer_tokenizer is None:
        return None
    try:
        import torch
        inputs = _transformer_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = _transformer(**inputs)
            logits = outputs.logits[0].cpu().numpy()
        # convert logits to probabilities (softmax)
        import numpy as np
        probs = np.exp(logits - np.max(logits))
        probs = probs / probs.sum()
        label_idx = int(probs.argmax())
        confidence = float(probs[label_idx])
        return {"label": str(label_idx), "confidence": confidence, "source": "transformer"}
    except Exception as e:
        logger.exception("Transformer prediction failed: %s", e)
        return None


def predict(text: str) -> Dict[str, Any]:
    """
    Unified predict function. Returns a dict that the API expects.
    This is the symbol main.py imports: `from .model import predict`
    """
    text = text or ""
    # 1) baseline
    try:
        r = _predict_baseline(text)
        if r:
            return {"label": r["label"], "confidence": r["confidence"], "source": r["source"], "message": "ok"}
    except Exception:
        logger.exception("Error in baseline prediction")

    # 2) transformer
    try:
        r = _predict_transformer(text)
        if r:
            return {"label": r["label"], "confidence": r["confidence"], "source": r["source"], "message": "ok"}
    except Exception:
        logger.exception("Error in transformer prediction")

    # fallback
    return {"label": "unknown", "confidence": 0.0, "source": "fallback", "message": "model not loaded"}
