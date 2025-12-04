from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from torch.nn.functional import softmax

# Load your fine-tuned model
model_path = "./finetuned-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    scores = softmax(outputs.logits, dim=1).squeeze()
    labels = ['bearish', 'neutral', 'bullish']
    return {
        "sentiment": labels[torch.argmax(scores)],
        "scores": dict(zip(labels, scores.tolist()))
    }
