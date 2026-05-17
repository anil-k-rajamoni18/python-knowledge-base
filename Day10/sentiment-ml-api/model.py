from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from scipy.special import softmax
from schema import SentimentResponse

class SentimentModel:
    def __init__(self):
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

    def predict(self, text: str) -> SentimentResponse:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.model(**inputs)
        scores = outputs.logits[0].detach().numpy()
        probabilities = softmax(scores)

        label = "positive" if probabilities[1] > probabilities[0] else "negative"

        return SentimentResponse(
            label=label,
            positive=float(probabilities[1]),
            negative=float(probabilities[0])
        )
