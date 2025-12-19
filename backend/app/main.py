# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import importlib
import logging
from typing import Any, Callable, Dict

log = logging.getLogger("backend.app.main")

app = FastAPI(title="LucidVerify Fact Checker API")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# CORS: allow local dev origins (adjust for production)
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] for temporary dev convenience
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Try to import your model module
MODEL_MODULE = "backend.app.model"  # keep this unless your model is at a different path

_predict_fn: Callable[[str], Any] | None = None
_model_module = None

try:
    _model_module = importlib.import_module(MODEL_MODULE)
    # list candidate function names we might expect
    candidates = ["predict", "predict_text", "predict_route", "predict_from_text", "predict_fn"]
    for name in candidates:
        fn = getattr(_model_module, name, None)
        if callable(fn):
            _predict_fn = fn
            log.info("Using prediction function: %s.%s", MODEL_MODULE, name)
            break
    # also accept a module-level object named 'Model' with a predict method
    if _predict_fn is None:
        ModelClass = getattr(_model_module, "Model", None)
        if ModelClass is not None:
            inst = ModelClass() if callable(ModelClass) else ModelClass
            if hasattr(inst, "predict") and callable(inst.predict):
                _predict_fn = inst.predict
                log.info("Using Model.predict from %s", MODEL_MODULE)
except Exception as e:
    log.exception("Failed to import model module %s: %s", MODEL_MODULE, e)

@app.get("/", tags=["health"])
async def root():
    return {"message": "LucidVerify Fact Checker API is running"}

@app.post("/predict")
async def predict_route(payload: Dict[str, Any]):
    """
    Expects JSON: {"text": "..."}.
    If a real predict function is found in backend.app.model it's called with the
    raw text argument. Otherwise returns a helpful fallback result.
    """
    text = payload.get("text", "")
    if not isinstance(text, str):
        raise HTTPException(status_code=422, detail="Missing or invalid 'text' field")

    if _predict_fn is None:
        # No model function found — return fallback but keep format compatible.
        log.warning("No predict function available in %s", MODEL_MODULE)
        return {"label": "unknown", "confidence": 0.0, "source": "fallback", "message": "model not loaded"}
    try:
        # Try calling predict; many projects either accept text or a dict.
        try:
            result = _predict_fn(text)
        except TypeError:
            # try passing the whole payload instead
            result = _predict_fn(payload)

        # If the model returns a scalar or other type, coerce to expected dict.
        if isinstance(result, dict):
            return result
        else:
            # best-effort: assume (label, confidence) tuple or single label
            if isinstance(result, (list, tuple)) and len(result) >= 2:
                return {"label": str(result[0]), "confidence": float(result[1]), "source": "model"}
            return {"label": str(result), "confidence": 1.0, "source": "model"}
    except Exception as e:
        log.exception("Predict function raised an exception")
        return {"label": "unknown", "confidence": 0.0, "source": "error", "error": str(e)}
    from pydantic import BaseModel
