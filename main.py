import re
import hashlib
from sentiment_analysis import analyze_sentiment  # Assuming you have a sentiment analysis module
from nitter_scraper import scrape_user_tweets  
import pandas as pd
from trading_operations import get_alpaca_tickers



def contains_ticker(text):
    # Matches things like TSLA, NVDA
    return bool(re.search(r'\b[A-Z]{2,5}\b', text))

def get_tickers(text):
    return re.findall(r'\b[A-Z]{2,5}\b', text)


def hash_text(text):
    """Returns a SHA-256 hash of the input text."""
    return hashlib.sha256(text.encode()).hexdigest()

def get_valid_tickers(text):
    alpaca_tickers = get_alpaca_tickers()
    candidates = get_tickers(text)
    return [c for c in candidates if c in alpaca_tickers]

def tweet_filter(tweet, seen_tweets):
    tweet_text = tweet
    tweet_hash = hash_text(tweet_text)

    if tweet_hash in seen_tweets:
        return None, None

    seen_tweets.add(tweet_hash)
    with open("seen_tweets.txt", "a") as f:
        f.write(tweet_hash + "\n")

    tickers = get_valid_tickers(tweet_text)
    return tweet_text, tickers if tickers else []

    
    

    

def main():
    #TODO: Add a proxy controller to rotate proxies

    # users_to_scrape = ["unusual_whales"]

    # with open("valid_https_proxies.txt") as f:
    #     PROXIES = [line.strip() for line in f if line.strip()]

    # # Gets last page of tweets from the user unfilterd
    # tweets = scrape_user_tweets(users_to_scrape,PROXIES)

    df = pd.read_csv("financial_sentiment_dataset.csv")
    tweets = df.sample(10)["text"].tolist()

    try:
        with open("seen_tweets.txt", "r") as f:
            seen_tweets = set(f.read().splitlines())
    except FileNotFoundError:
        seen_tweets = set()

    for tweet in tweets:
        tweet_text, tickers = tweet_filter(tweet, seen_tweets=seen_tweets)
        if tweet_text is None:
            continue  # Already seen

        if tickers:
            print(analyze_sentiment(tweet))
            print(f"{tweet_text}\n→ Tickers: {', '.join(tickers)}\n")
            
        else:
            print(f"{tweet_text}\n→ No tickers found.\n")

    
   

if __name__ == "__main__":
    main()
