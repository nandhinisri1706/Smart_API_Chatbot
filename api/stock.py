import requests
import os


def get_stock_price(symbol):

    api_key = os.getenv("FINNHUB_API_KEY")

    if not api_key:
        return {
            "error": "FINNHUB_API_KEY is not configured"
        }

    symbol = symbol.upper()

    url = "https://finnhub.io/api/v1/quote"

    params = {
        "symbol": symbol,
        "token": api_key
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        return {
            "error": "Unable to fetch stock data"
        }

    data = response.json()

    if not data or data.get("c") is None:
        return {
            "error": "Stock data not available"
        }

    return {
        "symbol": symbol,
        "current_price": data.get("c"),
        "change": data.get("d"),
        "percent_change": data.get("dp"),
        "high": data.get("h"),
        "low": data.get("l"),
        "open": data.get("o"),
        "previous_close": data.get("pc")
    }