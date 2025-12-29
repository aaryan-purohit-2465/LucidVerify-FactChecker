from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.model import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict_route(data: dict):
    text = data.get("text", "")
    return predict(text)
