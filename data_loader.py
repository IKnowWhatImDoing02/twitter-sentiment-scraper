from datasets import load_dataset
import pandas as pd

# Load the dataset from Hugging Face
dataset = load_dataset("zeroshot/twitter-financial-news-sentiment", split="train")

# Convert to Pandas DataFrame
df = pd.DataFrame(dataset)

# Save to CSV for reuse
df.to_csv("financial_sentiment_dataset.csv", index=False)
print("Dataset saved as financial_sentiment_dataset.csv")
