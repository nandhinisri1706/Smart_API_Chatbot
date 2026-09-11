import requests


def get_gold_price():

    # Get current gold price in USD per ounce
    url = "https://api.gold-api.com/price/XAU"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return {
            "error": "Unable to fetch gold price"
        }

    data = response.json()

    gold_usd = data.get("price")

    if gold_usd is None:
        return {
            "error": "Gold price not available"
        }

    # Get USD to INR exchange rate
    currency_url = "https://api.frankfurter.dev/v2/rate/USD/INR"

    currency_response = requests.get(
        currency_url,
        timeout=10
    )

    currency_data = currency_response.json()

    usd_inr = currency_data["rate"]

    # 1 troy ounce = 31.1035 grams
    gold_inr_per_gram = (gold_usd * usd_inr) / 31.1035

    return {
        "usd_per_ounce": gold_usd,
        "usd_inr": usd_inr,
        "inr_per_gram": gold_inr_per_gram
    }