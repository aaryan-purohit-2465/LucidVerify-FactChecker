from fastapi import FastAPI
from pydantic import BaseModel
from backend.app.model import load_model, predict

app = FastAPI()

# ---------------------------
# Request Body Schema
# ---------------------------
class NewsRequest(BaseModel):
    text: str


# ---------------------------
# Startup: Load ML Model
# ---------------------------
@app.on_event("startup")
def startup_event():
    print("🔄 Loading ML pipeline model...")
    load_model()
    print("✅ Model loaded successfully")


# ---------------------------
# Health Check
# ---------------------------
@app.get("/")
def root():
    return {"status": "LucidVerify Backend Running"}


# ---------------------------
# Prediction Endpoint
# ---------------------------
@app.post("/predict")
def predict_news(req: NewsRequest):
    try:
        result = predict(req.text)
        return result
    except Exception as e:
        return {
            "label": "error",
            "confidence": 0.0,
            "source": "server_error",
            "message": str(e)
        }
