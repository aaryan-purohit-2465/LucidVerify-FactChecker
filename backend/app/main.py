# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.model import load_model, predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str


@app.on_event("startup")
def startup_event():
    load_model()


@app.post("/predict")
def predict_api(data: TextInput):
    return predict(data.text)
