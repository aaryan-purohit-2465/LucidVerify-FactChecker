# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.model import predict

app = FastAPI(title="LucidVerify – Fact Checker API")

# CORS (allow frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class PredictRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "LucidVerify API is running"}


@app.post("/predict")
def predict_route(request: PredictRequest):
    return predict(request.text)
