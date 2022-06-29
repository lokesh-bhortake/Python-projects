import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "YOUR_STOCK_API_KEY_HERE"
STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE"
NEWS_PARAMETERS = {
    "qInTitle": COMPANY_NAME,
    "apikey": NEWS_API_KEY,
}

TWILIO_SID = "YOUR_TWILIO_SID_HERE"
TWILIO_TOKEN = "YOUR_TWILIO_TOKEN_HERE"

stock_response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_data = stock_data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

dby_data = stock_data_list[1]
dby_closing_price = float(dby_data["4. close"])

diff = yesterday_closing_price - dby_closing_price
up_down = None
if diff > 0:
    up_down = "👆"
else:
    up_down = "👇"

percentage_diff = round(diff/dby_closing_price * 100)

if abs(percentage_diff) > 0:
    news_response = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    news_response.raise_for_status()
    news_articles = news_response.json()["articles"]

    three_articles = news_articles[:3]

    msg = [f"{STOCK_NAME}: {up_down}{percentage_diff}%\nHeadline : {article['title']} \nDescription : {article['description']} " for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_TOKEN)
    for i in range(3):
        message = client.messages.create(
            body=msg[i],
            from_="YOUR_NUMBER_PROVIDED_BY_API",
            to="RECIEVER_NUMBER",
        )

