from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.model import load_model, predict


app = FastAPI(title="LucidVerify API")

# CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    text: str


@app.on_event("startup")
def startup():
    load_model()


@app.get("/")
def root():
    return {"message": "LucidVerify backend running"}


@app.post("/predict")
def predict_news(req: PredictRequest):
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