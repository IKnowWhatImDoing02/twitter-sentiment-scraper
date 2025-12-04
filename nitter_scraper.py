import requests
import random
from bs4 import BeautifulSoup
import time
import hashlib

# Hardcoded list of working Nitter instances
NITTER_INSTANCES = [
    "https://xcancel.com/",
    "https://nitter.space/",
    "https://nitter.net/",
    "https://nitter.privacyredirect.com/",
    "https://lightbrd.com/",
    "https://nitter.poast.org/",
    "https://nitter.tiekoetter.com/",
]



# Scraping function
def scrape_user_tweets(users_to_scrape, PROXIES):
    for username in users_to_scrape: # e.g. unusual_whales
        for attempt in range(10):  # retry up to 10 times
            base_url = random.choice(NITTER_INSTANCES)
            proxy_addr = random.choice(PROXIES)
            proxies = {"http": proxy_addr, "https": proxy_addr}
            url = f"{base_url}/{username}"

            try:
                print(f"Attempting {url} with proxy {proxy_addr}")
                response = requests.get(url, proxies=proxies, timeout=10)
                if response.status_code == 429:
                    print("Rate limited, retrying with new instance and proxy...")
                    continue
                elif response.status_code != 200:
                    print(f"Failed with status code {response.status_code}")
                    continue

                soup = BeautifulSoup(response.text, "html.parser")
                tweets = soup.find_all("div", class_="timeline-item")
                tweet_list = []

                for tweet in tweets:
                    if tweet.find("div", class_="pinned"):
                        continue  # skip pinned tweets

                    valid_tweet = tweet.find("div", class_="tweet-content media-body")
                    tweet_list.append(valid_tweet)



                print(len(tweet_list), "tweets found on this page")
                if not tweet_list:
                    print("No tweets found — page structure may have changed or proxy was blocked.")
                    continue
                
                return tweet_list

            except Exception as e:
                print(f"Error: {e}")
                continue





if __name__ == "__main__":
    print("Scraper started")
    scrape_user_tweets()
