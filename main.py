# Weather Notifier
import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables
load_dotenv()

# Constants
GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_FORECAST_API_URL = "http://api.openweathermap.org/data/2.5/forecast"


# Get city latitude and longitude function
def get_city_coordinates(city_name: str) -> dict:
    """
    This function makes an API call to retrieve the city latitude and longitude details and
    return it as dictionary
    """

    geocoding_params = {
        "q": city_name,
        "appid": os.environ.get("OPENWEATHERMAP_API_KEY"),
        "limit": 1
    }

    # Get latitude and longitude of a given city using geocoding api
    geocoding_response = requests.get(url=GEOCODING_API_URL, params=geocoding_params)
    geocoding_response.raise_for_status()
    city_coordinates = geocoding_response.json()[0]
    return {
        "city": city_coordinates.get("name"),
        "latitude": city_coordinates.get("lat"),
        "longitude": city_coordinates.get("lon"),
        "state": city_coordinates.get("state"),
        "country": city_coordinates.get("country"),
    }


# Get weather forecast for a given city for the next 12 hours
def is_rainy_today(city_details: dict) -> bool:
    """
    This function retrieves the weather data for the next 12 hours using Open Weather Map API
    """
    weather_params = {
        "lat": city_details.get("latitude"),
        "lon": city_details.get("longitude"),
        "appid": os.environ.get("OPENWEATHERMAP_API_KEY"),
        "cnt": 5
    }

    weather_response = requests.get(url=WEATHER_FORECAST_API_URL, params=weather_params)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    is_rainy = False
    for w in weather_data["list"]:
        main_weather = w["weather"][0]
        print(f"Weather at: {w["dt_txt"]} -> {main_weather["main"]}, {main_weather["description"]}")
        if main_weather["id"] < 700:
            is_rainy = True

    return is_rainy


# Send SMS to notify weather conditions
def send_sms():
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today, remember to bring an umbrella☂️!",
        from_=os.environ.get("TWILIO_PHONE_NUMBER"),
        to=os.environ.get("MY_PHONE_NUMBER")
    )
    print(message.status)


# Get City details and weather status
city = get_city_coordinates("Mumbai")
weather = is_rainy_today(city)

# Send Whatsapp message to notify weather condition
if is_rainy_today(city):
    print("It's going to rain today, remember to bring an umbrella☂️!")
    send_sms()
