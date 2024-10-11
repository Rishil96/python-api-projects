# Stock News Alert
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

STOCK = "TATAMOTORS"
COMPANY_NAME = "Tata Motors"
EXCHANGE_NAME = ".BSE"

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
STOCK_DETAILS_API_ENDPOINT = "https://www.alphavantage.co/query"
stock_details_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK + EXCHANGE_NAME,
    "apikey": os.environ.get("ALPHA_VANTAGE_API_KEY")
}

# Get yesterday's and day before yesterday's date in the format yyyy-mm-dd
today = datetime.now()
yesterday = today - timedelta(days=1)
day_before_yesterday = yesterday - timedelta(days=1)

today = today.strftime("%Y-%m-%d")
yesterday = yesterday.strftime("%Y-%m-%d")
day_before_yesterday = day_before_yesterday.strftime("%Y-%m-%d")

# Get stock price details for yesterday and day before yesterday
stock_details_response = requests.get(url=STOCK_DETAILS_API_ENDPOINT, params=stock_details_params)
stock_details_response.raise_for_status()
stock_data = stock_details_response.json()

stock_price_yesterday = stock_data["Time Series (Daily)"][yesterday]["4. close"]
stock_price_yesterday = float(stock_price_yesterday)

stock_price_day_before_yesterday = stock_data["Time Series (Daily)"][day_before_yesterday]["4. close"]
stock_price_day_before_yesterday = float(stock_price_day_before_yesterday)

percentage_change = (stock_price_yesterday - stock_price_day_before_yesterday) / stock_price_day_before_yesterday * 100
print(f"Percentage change for {COMPANY_NAME} is {round(percentage_change, 2)}%")

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
news_params = {
    "q": COMPANY_NAME,
    "from": yesterday,
    "sortBy": "popularity",
    "apiKey": os.environ.get("NEWS_API_KEY")
}

news_response = requests.get(url=NEWS_API_ENDPOINT, params=news_params)
news_response.raise_for_status()
news_data = news_response.json()
top_3_articles = news_data["articles"][:3]

for article in top_3_articles:
    print(article)
    formatted_article = f"""
    Source: {article["source"]["name"]}
    Title: {article["title"]}
    Full Article: {article["url"]}
    Published at: {article["publishedAt"]}
    """

# STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
 by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
 coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of 
the coronavirus market crash.
"""
