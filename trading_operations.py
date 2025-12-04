import requests

ALPACA_API_KEY = "PKHBLUWRIZQKF4NXELAZ"
ALPACA_SECRET_KEY = "3cwv6lCIyFvXclEIfrNC1El6SHtlokcEUgX7ggdq"

headers = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY,
}

response = requests.get("https://paper-api.alpaca.markets/v2/assets", headers=headers)
assets = response.json()



def get_alpaca_tickers():
    tickers = {asset["symbol"] for asset in assets if asset["tradable"] and asset["status"] == "active"}
    return tickers