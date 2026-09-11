import streamlit as st
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from api.weather import get_weather
from api.gold import get_gold_price
from api.stock import get_stock_price
from api.currency import convert_currency


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN:
    client = InferenceClient(
        api_key=HF_TOKEN,
        provider="auto"
    )
else:
    client = None


# --------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart API Chatbot",
    page_icon="💬",
    layout="centered"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("Smart API Chatbot")

st.write(
    "Ask about weather, gold, stocks, currency or general topics."
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# WEATHER RESPONSE
# --------------------------------------------------

def weather_response(city):

    result = get_weather(city)

    if "error" in result:
        return result["error"]

    return f"""
### Weather in {result['city']}, {result['country']}

**Temperature:** {result['temperature']} °C

**Feels Like:** {result['feels_like']} °C

**Humidity:** {result['humidity']} %

**Wind Speed:** {result['wind_speed']} km/h

**Weather Code:** {result['weather_code']}
"""


# --------------------------------------------------
# GOLD RESPONSE
# --------------------------------------------------

def gold_response():

    result = get_gold_price()

    if "error" in result:
        return result["error"]

    return f"""
### Current Gold Price

**Gold Price:** ${result['usd_per_ounce']:,.2f} / troy ounce

**USD → INR:** ₹{result['usd_inr']:,.2f}

**Approx. Gold Price:** ₹{result['inr_per_gram']:,.2f} / gram

*This is an international spot-price based estimate, not a jewellery-shop retail rate.*
"""


# --------------------------------------------------
# STOCK RESPONSE
# --------------------------------------------------

def stock_response(symbol):

    result = get_stock_price(symbol)

    if "error" in result:
        return result["error"]

    return f"""
### Stock: {result['symbol']}

**Current Price:** ${result['current_price']:,.2f}

**Change:** {result['change']:,.2f}

**Change %:** {result['percent_change']:,.2f}%

**Day High:** ${result['high']:,.2f}

**Day Low:** ${result['low']:,.2f}

**Open:** ${result['open']:,.2f}

**Previous Close:** ${result['previous_close']:,.2f}
"""


# --------------------------------------------------
# CURRENCY RESPONSE
# --------------------------------------------------

def currency_response(amount, from_currency, to_currency):

    result = convert_currency(
        amount,
        from_currency,
        to_currency
    )

    if "error" in result:
        return result["error"]

    return f"""
### Currency Conversion

**Amount:** {result['amount']} {result['from']}

**Exchange Rate:** 1 {result['from']} = {result['rate']} {result['to']}

**Converted Amount:** {result['converted']:,.2f} {result['to']}

**Rate Date:** {result['date']}
"""


# --------------------------------------------------
# GENERAL CHAT USING HUGGING FACE
# --------------------------------------------------

def general_chat(user_message):

    if client is None:
        return (
            "Hugging Face token is not configured. "
            "Please add HF_TOKEN to your .env file."
        )

    try:

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful general-purpose AI assistant. "
                    "Answer clearly, accurately and concisely."
                )
            }
        ]

        # Add previous conversation
        for message in st.session_state.messages[-10:]:

            messages.append({
                "role": message["role"],
                "content": message["content"]
            })

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:fastest",
            messages=messages,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"General chat error: {str(e)}"


# --------------------------------------------------
# QUERY DETECTION
# --------------------------------------------------

def process_query(query):

    text = query.lower().strip()


    # ==================================================
    # WEATHER
    # ==================================================

    weather_words = [
        "weather",
        "temperature",
        "climate",
        "rain",
        "humidity",
        "wind"
    ]

    if any(word in text for word in weather_words):

        words = text.replace("?", "").split()

        city = None

        if "in" in words:

            index = words.index("in")

            if index + 1 < len(words):

                city = " ".join(words[index + 1:])

        if city:

            return weather_response(city)

        return (
            "Please mention a city.\n\n"
            "Example: `What is the weather in Chennai?`"
        )


    # ==================================================
    # GOLD
    # ==================================================

    gold_words = [
        "gold price",
        "gold rate",
        "gold",
        "24k",
        "22k"
    ]

    if any(word in text for word in gold_words):

        return gold_response()


    # ==================================================
    # STOCK
    # ==================================================

    stock_words = [
        "stock price",
        "share price",
        "stock",
        "share"
    ]

    if any(word in text for word in stock_words):

        words = text.replace("?", "").split()

        common_stocks = [
            "aapl",
            "msft",
            "tsla",
            "nvda",
            "amzn",
            "googl",
            "meta"
        ]

        for stock in common_stocks:

            if stock in words:

                return stock_response(
                    stock.upper()
                )

        return (
            "Please provide a stock symbol.\n\n"
            "Examples:\n"
            "- `What is AAPL stock price?`\n"
            "- `What is TSLA stock price?`"
        )


    # ==================================================
    # CURRENCY
    # ==================================================

    currency_words = [
        "currency",
        "exchange rate",
        "convert",
        "usd to",
        "inr to",
        "eur to",
        "gbp to"
    ]

    if any(word in text for word in currency_words):

        words = text.replace("?", "").split()

        if "to" in words:

            index = words.index("to")

            if index > 0 and index + 1 < len(words):

                from_currency = words[index - 1].upper()
                to_currency = words[index + 1].upper()

                amount = 1.0

                for word in words:

                    try:

                        amount = float(word)
                        break

                    except ValueError:

                        pass

                return currency_response(
                    amount,
                    from_currency,
                    to_currency
                )

        return (
            "Please specify the currencies.\n\n"
            "Example: `100 USD to INR`"
        )


    # ==================================================
    # GENERAL CHAT
    # ==================================================

    return general_chat(query)


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_prompt = st.chat_input(
    "Ask something..."
)


# --------------------------------------------------
# PROCESS USER MESSAGE
# --------------------------------------------------

if user_prompt:

    # Display user message
    with st.chat_message("user"):

        st.markdown(user_prompt)


    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })


    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Processing..."):

            response = process_query(user_prompt)

        st.markdown(response)


    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })