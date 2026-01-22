from fastapi import FastAPI
from pydantic import BaseModel
from backend.app.model import load_model, predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LucidVerify AI Backend")

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later we can restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NewsRequest(BaseModel):
    text: str


@app.on_event("startup")
def startup():
    print("Starting backend...")
    load_model()
    print("Backend ready!")


@app.get("/")
def home():
    return {"message": "LucidVerify AI Backend is running"}


@app.post("/predict")
def predict_news(request: NewsRequest):
    try:
        result = predict(request.text)
        return result
    except Exception as e:
        return {
            "label": "error",
            "confidence": 0.0,
            "source": "server_error",
            "message": str(e)
        }
