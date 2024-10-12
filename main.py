# Stock News Alert
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

STOCK = "RELIANCE"
COMPANY_NAME = "Reliance Industries"
EXCHANGE_NAME = ".BSE"
STOCK_DETAILS_API_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"

# Get yesterday's and day before yesterday's date in the format yyyy-mm-dd
today = datetime.now()
yesterday = today - timedelta(days=1)
day_before_yesterday = yesterday - timedelta(days=1)

today = today.strftime("%Y-%m-%d")
yesterday = yesterday.strftime("%Y-%m-%d")
day_before_yesterday = day_before_yesterday.strftime("%Y-%m-%d")

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_stock_percentage_change(stock_name: str, exchange_name: str) -> float:
    stock_details_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_name + exchange_name,
        "apikey": os.environ.get("ALPHA_VANTAGE_API_KEY")
    }

    # Get stock price details for yesterday and day before yesterday
    stock_details_response = requests.get(url=STOCK_DETAILS_API_ENDPOINT, params=stock_details_params)
    stock_details_response.raise_for_status()
    stock_data = stock_details_response.json()

    stock_price_yesterday = stock_data["Time Series (Daily)"][yesterday]["4. close"]
    stock_price_yesterday = float(stock_price_yesterday)

    stock_price_day_before_yesterday = stock_data["Time Series (Daily)"][day_before_yesterday]["4. close"]
    stock_price_day_before_yesterday = float(stock_price_day_before_yesterday)

    percentage_change = (stock_price_yesterday - stock_price_day_before_yesterday) / stock_price_day_before_yesterday * 100
    print(f"Percentage change for {stock_name} is {round(percentage_change, 2)}%")
    return round(percentage_change, 2)



# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

def get_stock_news(company_name, news_date) -> list:
    """
    Get top 3 news articles on the stock/company
    """

    news_params = {
        "q": company_name,
        "from": news_date,
        "sortBy": "popularity",
        "apiKey": os.environ.get("NEWS_API_KEY")
    }

    news_response = requests.get(url=NEWS_API_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    top_3_articles = news_data["articles"][:3]

    formatted_articles = []
    for index in range(len(top_3_articles)):
        article = top_3_articles[index]
        formatted_article = f"""
        {index + 1}. {article["title"]}
        Source: {article["source"]["name"]}
        Full Article: {article["url"]}
        Published at: {article["publishedAt"]}
        """
        formatted_articles.append(formatted_article)

    return formatted_articles


# STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.
def send_stock_update_sms() -> None:
    """
    This function sends an SMS to the user notifying the drastic change in the stock price and related news
    """
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    stock_percent_change = get_stock_percentage_change(stock_name=STOCK, exchange_name=EXCHANGE_NAME)
    top_3_articles = get_stock_news(company_name=COMPANY_NAME, news_date=yesterday)

    direction_emoji = "🔺" if  stock_percent_change >= 0 else "🔻"
    body = f"{STOCK}: {direction_emoji}{abs(stock_percent_change)}%"

    for index in range(len(top_3_articles)):
        body += f"\n{top_3_articles[index]}"

    message = client.messages.create(
        body=body,
        from_=os.environ.get("TWILIO_PHONE_NUMBER"),
        to=os.environ.get("MY_PHONE_NUMBER"),
    )

    print(message.sid)


if __name__ == "__main__":
    send_stock_update_sms()

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
