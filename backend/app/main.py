from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.model import load_model, predict

app = FastAPI(title="LucidVerify API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsRequest(BaseModel):
    text: str


@app.on_event("startup")
def startup():
    load_model()


@app.get("/")
def home():
    return {"message": "LucidVerify API running"}


@app.post("/predict")
def verify_news(req: NewsRequest):
    result = predict(req.text)
    return result
