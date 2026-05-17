from fastapi import FastAPI
from schema import SentimentRequest, SentimentResponse
from model import SentimentModel

app = FastAPI(title="Real-Time Sentiment Analysis API")

# Load model once at startup
model = SentimentModel()

@app.get("/")
def home():
    return {"message": "Sentiment Analysis API is running!"}

@app.post("/analyze", response_model=SentimentResponse)
def analyze_sentiment(request: SentimentRequest):
    result = model.predict(request.text)
    return result

@app.get("/health")
def health_check():
    return {"status": "healthy"}