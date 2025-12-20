# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.model import predict

app = FastAPI(title="LucidVerify API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "LucidVerify backend running"}

@app.post("/predict")
def predict_route(payload: dict):
    text = payload.get("text", "")
    return predict(text)
