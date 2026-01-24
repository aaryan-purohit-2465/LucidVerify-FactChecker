from fastapi import FastAPI
from pydantic import BaseModel
from backend.app.model import load_model, predict

app = FastAPI(title="LucidVerify API")


class NewsRequest(BaseModel):
    text: str


@app.on_event("startup")
def startup_event():
    load_model()


@app.post("/predict")
def predict_news(req: NewsRequest):
    return predict(req.text)
