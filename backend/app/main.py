from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.model import analyze_text

app = FastAPI(
    title="LucidVerify Backend",
    description="AI-powered Fake News Detection API",
    version="1.0.0"
)

# Allow frontend access (Vercel / localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "LucidVerify backend is running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: NewsRequest):
    """
    Takes news text and returns:
    - label (real/fake/unknown)
    - confidence
    - source
    - explanation
    """
    return analyze_text(req.text)
