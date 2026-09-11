import requests


def get_currency_rate(from_currency, to_currency):

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    url = f"https://api.frankfurter.dev/v2/rate/{from_currency}/{to_currency}"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return {
            "error": "Currency rate not available"
        }

    data = response.json()

    return {
        "from": data["base"],
        "to": data["quote"],
        "rate": data["rate"],
        "date": data["date"]
    }


def convert_currency(amount, from_currency, to_currency):

    result = get_currency_rate(
        from_currency,
        to_currency
    )

    if "error" in result:
        return result

    converted_amount = amount * result["rate"]

    return {
        "amount": amount,
        "from": result["from"],
        "to": result["to"],
        "rate": result["rate"],
        "converted": converted_amount,
        "date": result["date"]
    }