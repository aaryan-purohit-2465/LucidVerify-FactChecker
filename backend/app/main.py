# backend/app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from .model import load_model, predict

app = FastAPI(title="LucidVerify Fact Checker API")


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    label: str
    confidence: float
    source: str


@app.on_event("startup")
def startup_event():
    load_model()


@app.get("/")
def root():
    return {"message": "LucidVerify Fact Checker API is running"}


@app.post("/predict", response_model=PredictResponse)
def predict_claim(request: PredictRequest):
    return predict(request.text)
