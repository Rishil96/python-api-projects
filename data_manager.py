import os
import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    FLIGHT_API_ENDPOINT = "https://api.sheety.co/d1d6eaca05258647c2e89ceecab654ce/flightDeals/prices"

    def __init__(self):
        self.flight_api_key = os.environ.get("FLIGHT_SHEET_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.flight_api_key}"
        }

    def get_city_table(self) -> list:
        """
        This method makes a get request to get all the cities along with prices for flight booking
        """
        response = requests.get(url=self.FLIGHT_API_ENDPOINT, headers=self.headers)
        response.raise_for_status()
        flight_data = response.json()
        return flight_data.get("prices")
