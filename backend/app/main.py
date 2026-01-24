from fastapi import FastAPI
from pydantic import BaseModel
from backend.app.model import load_model, predict

app = FastAPI()
@app.post("/predict")
def predict_news(req: NewsRequest):
    label, confidence, source = predict(req.text)
    return {
        "label": label,
        "confidence": confidence,
        "source": source
    }



class NewsRequest(BaseModel):
    text: str


@app.on_event("startup")
def startup_event():
    load_model()


@app.post("/predict")
def predict_news(req: NewsRequest):
    label, confidence, source = predict(req.text)  # ✅ raw string only
    return {
        "label": label,
        "confidence": confidence,
        "source": source
    }
