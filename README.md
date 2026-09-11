# Smart API Chatbot

## Project Overview

Smart API Chatbot is a Streamlit-based conversational application that combines general AI chat with real-time information retrieved from external APIs.

The application allows users to ask normal questions and also retrieve information such as weather conditions, gold prices, stock prices, and currency exchange rates through HTTP API requests.

<img width="670" height="578" alt="image" src="https://github.com/user-attachments/assets/59f1682f-a81f-4a48-bbb2-f4e76218cd39" />

## Features

* General AI conversation using Hugging Face
* Current weather information
* Current gold price information
* Stock price information
* Currency conversion
* Chat history during the current session
* REST API integration using Python
* JSON response processing
* Streamlit web interface
* Easy deployment using Streamlit Community Cloud

## Technologies Used

* Python
* Streamlit
* Hugging Face Inference API
* Finnhub Stock API
* Open-Meteo Weather API
* Gold API
* Frankfurter Currency API
* REST APIs
* HTTP GET Requests
* JSON
* python-dotenv

## Project Structure

```text
smart api chatbot/
│
├── api/
│   ├── currency.py
│   ├── gold.py
│   ├── stock.py
│   └── weather.py
│
├── app.py
├── requirements.txt
├── .env
└── .gitignore
```

## API Usage

### 1. Hugging Face

Hugging Face is used for general-purpose AI conversations.

Example:

```text
User:
What is Artificial Intelligence?

Response:
Artificial Intelligence is a field of computer science...
```

Required environment variable:

```env
HF_TOKEN=your_huggingface_token
```

### 2. Finnhub

Finnhub is used to retrieve stock market information.

Example:

```text
User:
What is AAPL stock price?
```

The application can return:

```text
Stock: AAPL

Current Price: $...
Change: ...
Change %: ...
Day High: $...
Day Low: $...
Open: $...
Previous Close: $...
```

Required environment variable:

```env
FINNHUB_API_KEY=your_finnhub_api_key
```

### 3. Open-Meteo

Open-Meteo is used for weather information.

No API key is required.

Example:

```text
User:
What is the weather in Chennai?
```

Example response:

```text
Weather in Chennai, India

Temperature: 30 °C
Feels Like: 34 °C
Humidity: 70 %
Wind Speed: 15 km/h
```

### 4. Gold API

Gold API is used to retrieve the current international gold spot price.

No API key is required for the current implementation.

Example:

```text
User:
What is the current gold price?
```

Example response:

```text
Current Gold Price

Gold Price: $... / troy ounce
USD → INR: ₹...
Approx. Gold Price: ₹... / gram
```

The displayed INR-per-gram value is an approximate conversion from international spot gold price and should not be treated as the exact jewellery-shop retail rate.

### 5. Frankfurter

Frankfurter is used for currency exchange rates.

No API key is required.

Example:

```text
User:
100 USD to INR
```

Example response:

```text
Currency Conversion

Amount: 100 USD
Exchange Rate: 1 USD = ... INR
Converted Amount: ... INR
Rate Date: ...
```

## How the Application Works

The application first receives the user's message through the Streamlit chat interface.

The query is then analyzed to determine the required service.

```text
User Query
    |
    v
Streamlit Chat Interface
    |
    v
Query Detection
    |
    +------------------+
    |                  |
    v                  v
API Request       General Question
    |                  |
    v                  v
External API       Hugging Face
    |
    v
JSON Response
    |
    v
Python Processing
    |
    v
Streamlit Response
```

## HTTP API Integration

The project demonstrates how Python can access external web services using HTTP requests.

Example:

```python
response = requests.get(url, params=params)
data = response.json()
```

The process is:

```text
Python
   |
   | HTTP GET Request
   v
External REST API
   |
   | JSON Response
   v
Python
   |
   v
Streamlit
   |
   v
User
```

## Installation

Clone or download the project and open the project folder in VS Code.

Install the required packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root directory.

```env
HF_TOKEN=your_huggingface_token
FINNHUB_API_KEY=your_finnhub_api_key
```

Do not upload the `.env` file to GitHub.

## Running the Application

Run the following command:

```bash
python -m streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

## Example Queries

### General Chat
<img width="621" height="569" alt="image" src="https://github.com/user-attachments/assets/e29203de-7016-4fef-9b6b-bcebd591c9a0" />

```text
What is Machine Learning?
```

```text
Explain Python in simple terms.
```

```text
What is a database?
```

### Weather
<img width="580" height="377" alt="image" src="https://github.com/user-attachments/assets/464afe41-d589-4245-8e9f-30417716a09a" />

```text
What is the weather in Chennai?
```

```text
What is the temperature in Mumbai?
```

### Gold
<img width="592" height="348" alt="image" src="https://github.com/user-attachments/assets/dd83969b-93ad-415e-bd3b-fa1fcb5963c0" />

```text
What is the current gold price?
```

```text
What is the gold rate?
```

### Stocks
<img width="565" height="410" alt="image" src="https://github.com/user-attachments/assets/aaba4554-3fc9-491b-b2bc-98efeafb86ff" />

```text
What is AAPL stock price?
```

```text
What is TSLA stock price?
```

```text
What is NVDA stock price?
```

### Currency
<img width="583" height="347" alt="image" src="https://github.com/user-attachments/assets/2e59d7f6-5d51-4113-b68d-d0ca926e19b9" />
```text
100 USD to INR
```

```text
500 EUR to INR
```

```text
1000 GBP to INR
```

## Example API Flow

For a weather query:

```text
User:
What is the weather in Chennai?

        ↓

Python detects "weather"

        ↓

Open-Meteo API

        ↓

HTTP GET Request

        ↓

JSON Response

        ↓

Python processes the data

        ↓

Streamlit displays the result
```

For a stock query:

```text
User:
What is AAPL stock price?

        ↓

Python detects stock query

        ↓

Finnhub API

        ↓

HTTP GET Request

        ↓

JSON Response

        ↓

Python processes stock data

        ↓

Streamlit displays the result
```

## Security

API keys should never be directly written inside Python source code.

Use environment variables:

```env
HF_TOKEN=your_token
FINNHUB_API_KEY=your_key
```

The `.gitignore` file should contain:

```text
.env
__pycache__/
*.pyc
.streamlit/
```

## Future Enhancements

* Voice input and output
* More financial APIs
* Cryptocurrency information
* News API integration
* Stock price charts
* Weather forecast
* Multiple AI model support
* Improved natural-language query detection
* Streamlit Cloud deployment
* Better error handling
* API response caching

## Conclusion

Smart API Chatbot demonstrates the integration of Python, HTTP requests, REST APIs, JSON data, external services, and Streamlit in a single application. It provides both general AI conversation and real-time information retrieval through external APIs.
