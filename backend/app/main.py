from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.model import load_model, predict

app = FastAPI(title="LucidVerify API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsRequest(BaseModel):
    text: str


@app.on_event("startup")
def startup_event():
    print("🚀 Starting LucidVerify backend...")
    success = load_model()
    if success:
        print("✅ Backend ready")
    else:
        print("❌ Backend failed to load model")


@app.get("/")
def home():
    return {"message": "LucidVerify API running"}


@app.post("/predict")
def verify(req: NewsRequest):
    return predict(req.text)
